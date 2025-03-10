class OptimizedApiClient:
    """Wrapper kolem Claude API klienta s optimalizacemi."""

    def __init__(self, client, cache_size=100, max_history_items=10):
        """
        Inicializuje optimalizovaný klient.

        Args:
            client: Základní Claude API klient
            cache_size (int): Velikost cache pro odpovědi
            max_history_items (int): Maximální počet zpráv v historii
        """
        self.client = client
        self.cache_size = cache_size
        self.max_history_items = max_history_items
        self.cache = {}  # prompt_hash -> odpověď
        self.cache_order = []  # LRU pořadí
        self.token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }

    def _hash_prompt(self, prompt, template_name=None, **params):
        """
        Vytvoří hash pro daný prompt a parametry.

        Args:
            prompt (str): Text promptu nebo template_name
            template_name (str, optional): Název šablony
            **params: Další parametry

        Returns:
            str: Hash reprezentující tento prompt
        """
        import hashlib
        import json

        # Vytvoření struktury pro hashování
        hash_data = {
            "prompt": prompt,
            "template": template_name,
            "params": params
        }

        # Serializace a hashování
        serialized = json.dumps(hash_data, sort_keys=True)
        return hashlib.md5(serialized.encode()).hexdigest()

    def _update_cache(self, prompt_hash, response):
        """
        Aktualizuje cache s novou odpovědí.

        Args:
            prompt_hash (str): Hash promptu
            response: Odpověď k uložení
        """
        # Pokud už hash existuje, odstraníme ho ze seznamu pořadí
        if prompt_hash in self.cache:
            self.cache_order.remove(prompt_hash)

        # Přidáme na konec seznamu (nejnovější)
        self.cache_order.append(prompt_hash)
        self.cache[prompt_hash] = response

        # Pokud je cache plná, odstraníme nejstarší položku
        if len(self.cache_order) > self.cache_size:
            oldest_hash = self.cache_order.pop(0)
            del self.cache[oldest_hash]

    def _trim_history(self, history):
        """
        Zkrátí historii na maximální počet položek.

        Args:
            history (list): Seznam zpráv v historii

        Returns:
            list: Zkrácená historie
        """
        if len(history) <= self.max_history_items:
            return history

        # Ponecháme první zprávu (často obsahuje důležité instrukce)
        # a pak poslední (max_history_items - 1) zpráv
        return [history[0]] + history[-(self.max_history_items - 1):]

    def send_message(self, message, history=None, use_cache=True):
        """
        Odešle zprávu s optimalizacemi.

        Args:
            message (str): Zpráva k odeslání
            history (list, optional): Historie konverzace
            use_cache (bool): Zda použít cache

        Returns:
            str: Odpověď od API
        """
        # Zkrácení historie pokud je potřeba
        if history:
            history = self._trim_history(history)

        # Vytvoření hashe pro cache
        prompt_hash = self._hash_prompt(message, history=history) if use_cache else None

        # Kontrola cache
        if use_cache and prompt_hash in self.cache:
            print("Použití cached odpovědi")
            return self.cache[prompt_hash]

        # Odeslání požadavku
        response = self.client.send_message(message, history=history)

        # Aktualizace statistik a cache
        if use_cache:
            self._update_cache(prompt_hash, response)

        # Aktualizace token usage (pokud API poskytuje tyto informace)
        if hasattr(self.client, 'last_token_usage'):
            self.token_usage["prompt_tokens"] += getattr(self.client, 'last_token_usage').get("input_tokens", 0)
            self.token_usage["completion_tokens"] += getattr(self.client, 'last_token_usage').get("output_tokens", 0)
            self.token_usage["total_tokens"] = self.token_usage["prompt_tokens"] + self.token_usage["completion_tokens"]

        return response

    def get_token_usage(self):
        """
        Vrátí statistiky využití tokenů.

        Returns:
            dict: Statistiky tokenů
        """
        return self.token_usage
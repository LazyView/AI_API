class ChainingManager:
    def __init__(self, client):
        self.client = client
        self.steps = []
        self.results = {}

    def add_step(self, name, template_name, input_mapping, output_key=None):
        """

        :param name: Unique name of the step
        :param template_name: Name of used template
        :param input_mapping: Input mapping for template (can contain references on previous steps).
        :param output_key: Save output as a key
        """
        self.steps.append({
            "name" : name,
            "template": template_name,
            "input_mapping": input_mapping,
            "output_key": output_key or name
        })

    def resolve_input(self, input_mapping):
        """
        :param input_mapping: Input mapping with possible references
        :return: dict: Evaluated inputs for template
        """
        resolved_inputs = {}

        for key, value in input_mapping.items():
            if  isinstance(value, str) and value.startswith("$"):
                # Previous step output reference
                ref_parts = value[1:].split(".")
                step_name = ref_parts[0]

                if step_name not in self.results:
                    raise ValueError(f"Step {step_name} was not made yet or doesn't have a result.")

                if len(ref_parts) > 1:
                    # Reference on special part of result
                    result = self.results[step_name]
                    for part in ref_parts[1:]:
                        if isinstance(result, dict) and part in result:
                            result = result[part]
                        else:
                            raise ValueError(f"Cannot find {part} in step {step_name} of the result.")
                    resolved_inputs[key] = result
                else:
                    # Apply whole result
                    resolved_inputs[key] = self.results[step_name]
            else:
                resolved_inputs[key] = value
        return resolved_inputs

    def execute(self, max_retries=1):
        """
        :param max_retries: Maximum number of tries for each step when failed
        :return: Result of all steps
        """
        for step in self.steps:
            name = step["name"]
            template = step["template"]
            input_mapping = step["input_mapping"]
            output_key = step["output_key"]

            print(f"Making step: {name}")

            try:
                resolved_inputs = self.resolve_input(input_mapping)
            except ValueError as e:
                print(f"Error while evaluating input for step {name} : {e}")
                break

            for attempt in range(max_retries + 1):
                try:
                    response = self.client.send_templated_message(template, **resolved_inputs)
                    self.results[output_key] = response
                    break
                except Exception as e:
                    if attempt < max_retries:
                        print(f"Attempt {attempt+1}/{max_retries+1} failed: {e}. Trying again...")
                    else:
                        print(f"All tries for step {name} failed: {e}")
                        return self.results
        return self.results
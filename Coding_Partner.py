from Claude_Client import ClaudeClient
from Optimized_Claude_Client import OptimizedApiClient
import re

class CodingPartner:
    """AI-powered coding assistant using Claude API."""

    def __init__(self, api_key=None):
        """Initialize the coding partner with Claude API client."""
        # Create our optimized client
        base_client = ClaudeClient()
        self.client = OptimizedApiClient(base_client)

        # Register code-related prompt templates
        self._register_templates()

    def _register_templates(self):
        """Register specialized templates for code-related tasks."""
        templates = {
            "analyze_code": """
                Analyze this {language} code and provide a comprehensive review:
                
                ```{language}
                {code}
                ```
                
                Please address the following areas:
                1. Code quality and organization
                2. Potential bugs or errors
                3. Performance considerations
                4. Security issues (if applicable)
                5. Recommendations for improvement
                
                Format your response with clear headings for each section.
            """,

            "optimize_code": """
                Optimize this {language} code while maintaining its functionality:
                
                ```{language}
                {code}
                ```
                
                Focus on these aspects:
                - Improving performance
                - Reducing complexity
                - Following best practices
                - Making it more readable
                
                Provide the optimized code and explain your changes.
            """,

            "generate_code": """
                Generate {language} code that accomplishes the following task:
                
                {requirement}
                
                Additional specifications:
                {specifications}
                
                Please provide well-structured, documented code with comments explaining key parts.
            """,

            "debug_code": """
                Debug this {language} code which has the following issue:
                
                Problem description: {problem}
                
                ```{language}
                {code}
                ```
                
                Identify the root cause and provide a fixed version of the code.
                Explain what was causing the issue and how your solution fixes it.
            """,

            "translate_code": """
                Translate this code from {source_language} to {target_language}:
                
                ```{source_language}
                {code}
                ```
                
                Maintain the same functionality and structure. Add comments to explain any significant changes
                required due to language differences.
            """,
        }

        # Register templates with the client
        for name, template_text in templates.items():
            self.client.client.prompt_manager.register_template(name, template_text)

    def analyze_code(self, code, language):
        """
        Analyze code and provide feedback.

        Args:
            code (str): The source code to analyze
            language (str): Programming language of the code

        Returns:
            dict: Structured analysis results
        """
        response = self.client.client.send_templated_message(
            "analyze_code",
            language=language,
            code=code
        )

        # For now, just return the raw response
        # In a more advanced implementation, we would parse this into a structured format
        return response

    def optimize_code(self, code, language):
        """
        Optimize the given code.

        Args:
            code (str): The source code to optimize
            language (str): Programming language of the code

        Returns:
            tuple: (optimized_code, explanation)
        """
        response = self.client.client.send_templated_message(
            "optimize_code",
            language=language,
            code=code
        )

        # Extract optimized code from response
        # This is a simplified extraction - a real implementation would be more robust

        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)

        if code_blocks:
            optimized_code = code_blocks[0].strip()
            # Get explanation by removing code blocks from response
            explanation = re.sub(r"```.*?```", "", response, flags=re.DOTALL).strip()
            return optimized_code, explanation
        else:
            return None, response

    def generate_code(self, requirement, language, specifications=""):
        """
        Generate code based on requirements.

        Args:
            requirement (str): Description of what the code should do
            language (str): Target programming language
            specifications (str): Additional specifications or constraints

        Returns:
            str: Generated code
        """
        response = self.client.client.send_templated_message(
            "generate_code",
            language=language,
            requirement=requirement,
            specifications=specifications
        )

        # Extract code from response
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)

        if code_blocks:
            return code_blocks[0].strip()
        else:
            return response  # Return full response if no code block found

    def debug_code(self, code, problem, language):
        """
        Debug code with a specific issue.

        Args:
            code (str): The problematic code
            problem (str): Description of the issue
            language (str): Programming language

        Returns:
            tuple: (fixed_code, explanation)
        """
        response = self.client.client.send_templated_message(
            "debug_code",
            language=language,
            code=code,
            problem=problem
        )

        # Extract fixed code from response
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)

        if code_blocks:
            fixed_code = code_blocks[0].strip()
            # Get explanation by removing code blocks from response
            explanation = re.sub(r"```.*?```", "", response, flags=re.DOTALL).strip()
            return fixed_code, explanation
        else:
            return None, response

    def translate_code(self, code, source_language, target_language):
        """
        Translate code from one language to another.

        Args:
            code (str): Source code to translate
            source_language (str): Original programming language
            target_language (str): Target programming language

        Returns:
            str: Translated code
        """
        response = self.client.client.send_templated_message(
            "translate_code",
            source_language=source_language,
            target_language=target_language,
            code=code
        )

        # Extract translated code from response
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)

        if code_blocks:
            return code_blocks[0].strip()
        else:
            return response  # Return full response if no code block found
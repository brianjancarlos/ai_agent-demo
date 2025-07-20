from colorama import Fore, Style

class Pipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, agent, method_name, output_variable):
        """Adds a step to the pipeline."""
        self.steps.append({
            "agent": agent,
            "method": method_name,
            "output_variable": output_variable
        })

    def run(self, initial_data: dict, verbose: bool = True):
        """Runs the pipeline."""
        data = initial_data.copy()

        for i, step in enumerate(self.steps):
            agent = step["agent"]
            method_name = step["method"]
            output_variable = step["output_variable"]

            if verbose:
                print(f"\n{Fore.YELLOW}>> Step {i+1}: Running {agent.name} Agent...{Style.RESET_ALL}")

            # Find the method in the agent instance
            method_to_call = getattr(agent, method_name)

            # This is a simple implementation. A more robust version would inspect the method
            # signature to determine the correct inputs to pass.
            # For now, we assume the method takes a single string argument.
            input_key = list(data.keys())[0] # Assume the first key is the input
            input_value = data[input_key]

            output = method_to_call(input_value)

            if verbose:
                # The agent methods now handle their own printing, so we just print a completion message.
                print(f"\n{Fore.GREEN}>> {agent.name} Agent finished.{Style.RESET_ALL}")

            data[output_variable] = output

        return data

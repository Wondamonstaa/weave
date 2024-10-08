import asyncio
import yaml
import logging
from weave.core.framework import SyntheticDataFramework
from weave.generators.programming_generator import ProgrammingGenerator
from weave.llm_interfaces.openai_provider import OpenAIProvider

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    # Load configuration
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Initialize components
    data_generator = ProgrammingGenerator()
    llm_provider = OpenAIProvider(**config['llm_provider']['params'])

    # Create framework
    framework = SyntheticDataFramework(data_generator, llm_provider)

    # Set custom prompt templates
    framework.set_prompt_template("question_generation", "Generate a {context[difficulty]} {context[language]} programming question about {context[topic]}. The answer should be: {answer}")
    framework.set_prompt_template("answer_validation", "For the {context[language]} question: {question}\nIs this a valid answer: {proposed_answer}? Answer with Yes or No.")

    # Generate dataset
    dataset = await framework.generate_dataset(config['framework']['num_samples'])

    # Validate dataset
    validations = await framework.validate_dataset(dataset)

    # Evaluate dataset
    criteria = {"aspect": "code_quality", "scale": "1-10"}
    evaluations = await framework.evaluate_dataset(dataset, criteria)

    # Print results
    print(f"Generated {len(dataset)} samples")
    print(f"First sample: {dataset[0]}")
    print(f"First validation: {validations[0]}")
    print(f"First evaluation: {evaluations[0]}")

    # Get model info
    print(f"Model info: {framework.get_model_info()}")
    print(f"Supported criteria: {framework.get_supported_criteria()}")

if __name__ == "__main__":
    asyncio.run(main())
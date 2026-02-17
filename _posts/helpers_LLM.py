import requests
import json
import argparse

def read_file(filename):
    """Read content from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise Exception(f"Error: {filename} not found")
    except IOError as e:
        raise Exception(f"Error reading {filename}: {str(e)}")

def save_output(content, filename):
    """Save content to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        raise Exception(f"Error saving to {filename}: {str(e)}")

def process_with_llm(api_url, api_key, user_prompt, user_text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek-chat",
        "messages": [{
            "role": "user",
            "content": f"{user_prompt}\n\n{user_text}"
        }],
        "temperature": 0.7,
        "max_tokens": 4096,
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def process_with_llm_from_files(config_file, prompt_file, content_file, output_file=None):
    """
    Process text with LLM using markdown files
    
    Args:
        config_file (str): Path to the configuration file containing API URL and key
        prompt_file (str): Path to prompt instructions file
        content_file (str): Path to content input file
        output_file (str, optional): Path to output results file. If None, only returns the result
        
    Returns:
        str: The LLM response text
    """
    try:
        # Load configuration
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Read input files
        prompt = read_file(prompt_file)
        content = read_file(content_file)
        
        # Process with LLM
        result = process_with_llm(
            config['api_url'],
            config['api_key'],
            prompt,
            content
        )
        
        # Save to file if output_file is provided
        if output_file:
            save_output(result, output_file)
            print(f"AI Response saved to {output_file}")
        
        return result
        
    except Exception as e:
        raise Exception(f"Error in process_with_llm_from_files: {str(e)}")

if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='Process text with LLM using markdown files')
    parser.add_argument('--config_file', default='config.json',
                      help='Path to configuration file (default: config.json)')
    parser.add_argument('--prompt_file', default='prompt.md', 
                      help='Path to prompt instructions file (default: prompt.md)')
    parser.add_argument('--content_file', default='content.md',
                      help='Path to content input file (default: content.md)')
    parser.add_argument('--output_file', default='output.md',
                      help='Path to output results file (default: output.md)')
    args = parser.parse_args()

    try:
        # Process with LLM
        result = process_with_llm_from_files(
            args.config_file,
            args.prompt_file,
            args.content_file,
            args.output_file
        )
        
        # Display results
        print(f"AI Response:\n{'-'*40}")
        print(result)
        print('-'*40)
        
    except Exception as e:
        print(str(e))
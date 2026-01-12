"""
Response Parser Module
Extracts structured data from AI responses
"""

import re

class ResponseParser:
    """Parses Gemini responses into structured task objects"""
    
    @staticmethod
    def parse_response(response_text):
        """Parse Gemini's response into structured task objects"""
        tasks = []
        
        task_blocks = re.split(r'TASK \d+:', response_text)
        task_blocks = [block.strip() for block in task_blocks if block.strip()]
        
        for block in task_blocks:
            try:
                task = ResponseParser._parse_task_block(block)
                if task.get('solution') and task.get('test_cases'):
                    tasks.append(task)
            except Exception as e:
                print(f"Error parsing task block: {e}")
                continue
        
        return tasks
    
    @staticmethod
    def _parse_task_block(block):
        """Parse a single task block"""
        task = {}
        
        # Extract title
        title_match = re.search(r'TITLE:\s*(.+?)(?:\n|$)', block)
        task['title'] = title_match.group(1).strip() if title_match else "Untitled"
        
        # Extract description
        desc_match = re.search(r'DESCRIPTION:\s*(.+?)(?=BUGGY_CODE:|CODE_WITH_BLANKS:|SOLUTION:|$)', block, re.DOTALL)
        task['description'] = desc_match.group(1).strip() if desc_match else ""
        
        # Extract buggy code (for fix_code tasks)
        buggy_match = re.search(r'BUGGY_CODE:\s*```cpp\s*(.+?)```', block, re.DOTALL)
        if buggy_match:
            task['buggy_code'] = buggy_match.group(1).strip()
        
        # Extract code with blanks (for fill_blank tasks)
        blank_match = re.search(r'CODE_WITH_BLANKS:\s*```cpp\s*(.+?)```', block, re.DOTALL)
        if blank_match:
            task['code_with_blanks'] = blank_match.group(1).strip()
        
        # Extract solution code
        solution_match = re.search(r'SOLUTION:\s*```cpp\s*(.+?)```', block, re.DOTALL)
        if solution_match:
            task['solution'] = solution_match.group(1).strip()
        else:
            # Fallback
            solution_alt = re.search(r'SOLUTION:\s*(.+?)(?=TEST_CASES:|---)', block, re.DOTALL)
            if solution_alt:
                task['solution'] = re.sub(r'```(?:cpp)?', '', solution_alt.group(1)).strip()
            else:
                task['solution'] = ""
        
        # Extract test cases
        task['test_cases'] = ResponseParser._parse_test_cases(block)
        
        return task
    
    @staticmethod
    def _parse_test_cases(block):
        """Parse test cases from a task block"""
        test_cases = []
        test_section = re.search(r'TEST_CASES:\s*(.+?)(?=---|TASK \d+:|$)', block, re.DOTALL)
        
        if test_section:
            test_text = test_section.group(1)
            pairs = re.findall(r'Input:\s*(.+?)\s*Expected Output:\s*(.+?)(?=Input:|$)', test_text, re.DOTALL)
            
            for inp, out in pairs:
                test_cases.append({
                    'input': inp.strip(),
                    'expected_output': out.strip()
                })
        
        return test_cases
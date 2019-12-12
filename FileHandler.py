
def is_java_file(file_path: str):
    if file_path.endswith('.java'):
        return True
    else:
        return False


def is_test_file(file_path: str):
    result = False
    if is_java_file(file_path):
        if '/' in file_path:
            path_split = file_path.split('/')
            file_name = file_path.split('/')[-1].split('.')[0]
        else:
            path_split = ''
            file_name = file_path.split('.')[0]

        if 'test' in path_split or file_name.startswith('Test') or file_name.endswith('Test')\
                or file_name.endswith('Tests') or file_name.endswith('TestCase')\
                or file_name.startswith('Mock') or file_name.endswith('Mock') or 'JUnit' in file_path:
            result = True
    return result

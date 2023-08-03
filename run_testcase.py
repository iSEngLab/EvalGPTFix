import glob
import os
import subprocess

import pandas as pd
from os import listdir


def cleanFiles(name):
    java_files = glob.glob('{}.*'.format(name))

    for file_path in java_files:
        os.remove(file_path)



def run_all_test_case(code, task, memory):
    path_to_test_case = "AtCoderTestCasesOfficial/" + task
    input_files = os.listdir(path_to_test_case + "/in")
    output_files = os.listdir(path_to_test_case + "/out")
    f_java = open("Main.java", 'a', encoding='utf-8')
    f_java.write(code)
    f_java.close()
    compile_result = subprocess.run(['javac', '-J-Dfile.encoding=UTF8', 'Main.java'], capture_output=True, text=True,
                                    encoding='utf-8')

    assert len(input_files) == len(output_files)
    if compile_result.returncode != 0:
        print("Compilation Error!")
        cleanFiles("Main")
        return [{'res':'CE'}]
    if len(input_files) == 0:
        print("No testcase to run!")
        cleanFiles("Main")
        return {'NT': "0/0"}
    else:
        num_test_case = (int)(len(input_files))
        count = 0
        res=[]
        for input_file, output_file in zip(input_files, output_files):
            input_path = path_to_test_case + "/in/" + input_file
            output_path = path_to_test_case + "/out/" + output_file
            input = open(input_path, 'r').read()
            expect_output = open(output_path, 'r').read()
            # 运行Java代码并向标准输入流中传递数据
            process = subprocess.Popen(['java', '-Xmx{}m'.format(memory), 'Main'], stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            try:
                actual_output, errors = process.communicate(input=input.encode('utf-8'), timeout=10)
            except subprocess.TimeoutExpired:
                print("Time Limit Exceed Error!")
                # cleanFiles("Main")
                res.append({'res': 'TLE', 'input': input, 'expect': expect_output})
                # res.append({'res': 'TLE'})
                process.kill()
                continue
                # return {'res': 'TLE', 'input': input, 'expect': expect_output}
            if errors.decode('utf-8') != '':
                if 'Invalid maximum heap size' in errors.decode('utf-8'):
                    print('Memory Limit Exceed')
                    res.append({'res': 'MLE', 'input': input, 'expect': expect_output})
                    # res.append({'res':'MLE'})
                    process.kill()
                    continue
                    # return {'res': 'MLE', 'input': input, 'expect': expect_output}
                else:
                    print("Runtime Error!")
                    res.append({'res':'RE', 'input':input, 'expect': expect_output})
                    # res.append({'res':'RE'})
                    process.kill()
                    continue
                    # return {'res':'RE', 'input':input, 'expect': expect_output}
                # return {'RE': errors.decode('utf-8')}
            # if actual_output.decode(encoding='utf-8').strip() == expect_output.strip():
            #     count += 1
            # else:
            #     print("One testcase failed!")
            #     print(expect_output)
            #     print(actual_output.decode(encoding='utf-8'))
            if not actual_output.decode(encoding='utf-8').strip() == expect_output.strip():
                print('Wrong Answer!')
                res.append({'res':'WA', 'input': input, 'expect': expect_output,'actual':actual_output.decode(encoding='utf-8')})
                # res.append({'res':'WA'})
                process.kill()
                continue
                # return {'res':'WA', 'input': input, 'expect': expect_output,'actual':actual_output.decode(encoding='utf-8')}

            res.append({'res':'AC'})
            process.kill()

        # print("All testcases passed!")
        cleanFiles("Main")
        for file_name in listdir('./'):
            if file_name.endswith('.class') or file_name.startswith('Main'):
                os.remove(file_name)

        # return {'res':'AC'}
        return res


def run_test_case(code, task, memory):
    path_to_test_case = "AtCoderTestCasesOfficial/" + task
    input_files = os.listdir(path_to_test_case + "/in")
    output_files = os.listdir(path_to_test_case + "/out")
    f_java = open("Main.java", 'a', encoding='utf-8')
    f_java.write(code)
    f_java.close()
    compile_result = subprocess.run(['javac', '-J-Dfile.encoding=UTF8', 'Main.java'], capture_output=True, text=True,
                                    encoding='utf-8')

    assert len(input_files) == len(output_files)
    if compile_result.returncode != 0:
        print("Compilation Error!")
        cleanFiles("Main")
        return {'res':'CE'}
    if len(input_files) == 0:
        print("No testcase to run!")
        cleanFiles("Main")
        return {'NT': "0/0"}
    else:
        num_test_case = (int)(len(input_files))
        count = 0
        res=[]
        for input_file, output_file in zip(input_files, output_files):
            input_path = path_to_test_case + "/in/" + input_file
            output_path = path_to_test_case + "/out/" + output_file
            input = open(input_path, 'r').read()
            expect_output = open(output_path, 'r').read()
            process = subprocess.Popen(['java', '-Xmx{}m'.format(memory), 'Main'], stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            try:
                actual_output, errors = process.communicate(input=input.encode('utf-8'), timeout=10)
            except subprocess.TimeoutExpired:
                print("Time Limit Exceed Error!")
                # cleanFiles("Main")
                # res.append({'res': 'TLE', 'input': input, 'expect': expect_output})
                # res.append({'res': 'TLE'})
                process.kill()
                # continue
                return {'res': 'TLE', 'input': input, 'expect': expect_output}
            if errors.decode('utf-8') != '':
                if 'Invalid maximum heap size' in errors.decode('utf-8'):
                    print('Memory Limit Exceed')
                    # res.append({'res': 'MLE', 'input': input, 'expect': expect_output})
                    # res.append({'res':'MLE'})
                    process.kill()
                    # continue
                    return {'res': 'MLE', 'input': input, 'expect': expect_output}
                else:
                    print("Runtime Error!")
                    # res.append({'res':'RE', 'input':input, 'expect': expect_output})
                    # res.append({'res':'RE'})
                    process.kill()
                    # continue
                    return {'res':'RE', 'input':input, 'expect': expect_output}
                # return {'RE': errors.decode('utf-8')}
            # if actual_output.decode(encoding='utf-8').strip() == expect_output.strip():
            #     count += 1
            # else:
            #     print("One testcase failed!")
            #     print(expect_output)
            #     print(actual_output.decode(encoding='utf-8'))
            if not actual_output.decode(encoding='utf-8').strip() == expect_output.strip():
                print('Wrong Answer!')
                # res.append({'res':'WA', 'input': input, 'expect': expect_output,'actual':actual_output.decode(encoding='utf-8')})
                # res.append({'res':'WA'})
                process.kill()
                # continue
                return {'res':'WA', 'input': input, 'expect': expect_output,'actual':actual_output.decode(encoding='utf-8')}

            # res.append({'res':'AC'})
            process.kill()

        print("All testcases passed!")
        cleanFiles("Main")
        for file_name in listdir('./'):
            if file_name.endswith('.class') or file_name.startswith('Main'):
                os.remove(file_name)

        return {'res':'AC'}
        # return res


if __name__ == '__main__':
    code = '''
import java.util.*;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String S = scanner.next();
        
        boolean condition1 = false;
        boolean condition2 = false;
        boolean condition3 = false;
        
        // Condition 1: Suppose that the x-th and y-th (x<y) characters from the left of S are B; then, x and y have different parities.
        for (int i = 0; i < S.length(); i++) {
            if (S.charAt(i) == 'B') {
                for (int j = i + 1; j < S.length(); j++) {
                    if (S.charAt(j) == 'B') {
                        if ((i % 2 == 0 && j % 2 == 1) || (i % 2 == 1 && j % 2 == 0)) {
                            condition1 = true;
                            break;
                        }
                    }
                }
            }
            if (condition1) {
                break;
            }
        }
        
        // Condition 2: K is between two R's
        for (int i = 0; i < S.length(); i++) {
            if (S.charAt(i) == 'R') {
                for (int j = i + 1; j < S.length(); j++) {
                    if (S.charAt(j) == 'R') {
                        for (int k = j + 1; k < S.length(); k++) {
                            if (S.charAt(k) == 'K') {
                                condition2 = true;
                                break;
                            }
                        }
                    }
                    if (condition2) {
                        break;
                    }
                }
            }
            if (condition2) {
                break;
            }
        }
        
        // Condition 3: Exactly one K and Q, and exactly two R's, B's, and N's
        int countK = 0;
        int countQ = 0;
        int countR = 0;
        int countB = 0;
        int countN = 0;
        for (int i = 0; i < S.length(); i++) {
            char c = S.charAt(i);
            if (c == 'K') {
                countK++;
            } else if (c == 'Q') {
                countQ++;
            } else if (c == 'R') {
                countR++;
            } else if (c == 'B') {
                countB++;
            } else if (c == 'N') {
                countN++;
            }
        }
        if (countK == 1 && countQ == 1 && countR == 2 && countB == 2 && countN == 2) {
            condition3 = true;
        }
        
        // Print the result
        if (condition1 && condition2 && condition3) {
            System.out.println("Yes");
        } else {
            System.out.println("No");
        }
    }
}
    '''
    task = "abc297/B"
    test_res=run_test_case(code, task, 1024)
    print(test_res)
    # for res in test_res:
    #     print(res)
    # print(run_test_case(code, task, 1024))

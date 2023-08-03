import openai
import csv
from run_testcase import run_test_case
from itertools import islice
import os
from os import listdir


openai.api_key='your api key'

base_prompt= "There's a bug in the program below. Try to fix it and return the complete fix for the code in the form of markdown code block.\n\n"
prompt_problem='The program is to solve this problem:\n'
prompt_ce="There's a Compilation Error in the code."
prompt_tle="The following input triggers a Time Limit Exceeded Error:\n"
prompt_mle="The following input triggers a Memory Limit Exceeded Error:\n"
prompt_re="The following input triggers a Runtime Error:\n"
prompt_wa="The following input triggers a Wrong Answer error:\n"
prompt_expect="The expected output is:\n"
prompt_actual="The actual output is:\n"
prompt_location= "There's a bug in the program below. Try to fix it and return the complete fix for the code in the form of markdown code block. The location of the bug is in or near the line with a comment \"//bug\".\n\n"
prompt_still_ce="There's still a Compilation Error in your code."
prompt_still_tle="There's still a Time Limit Exceeded Error in your code triggered by the input:\n"
prompt_still_mle="There's still a Memory Limit Exceeded Error in your code triggered by the input:\n"
prompt_still_re="There's still a Runtime Error in your code triggered by the input:\n"
prompt_still_wa="There's still a Wrong Answer error in your code triggered by the input:\n"
prompt_fix_again="Try to fix it again and return the complete fix for the code in the form of markdown code block."


data = open('data/latest_contests_new.csv', 'r')
reader = csv.reader(data)


def get_fix_from_gpt(query):
    success = False
    while not success:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            success = True
        except Exception as e:
            print(e)
            continue
    response = completion['choices'][0]['message']['content']
    flag = False
    fix_code = ''
    for res_line in response.split('\n'):
        if not flag:
            if res_line.startswith('```'):
                flag = True
            continue
        else:
            if res_line.startswith('```'):
                break
            fix_code += res_line
            fix_code += '\n'
    print(fix_code)
    return fix_code


def test_fix(query,bug_no,task):
    # os.mkdir('results_RQ2_problems/' + str(bug_no))
    for i in range(10,15):
        fix_code = get_fix_from_gpt(query)

        test_res = run_test_case(fix_code, task, 1024)
        res_file_path = 'results_RQ2_bug_location/' + str(bug_no) + '/'
        test_res_type = test_res['res']
        if test_res_type == 'AC' or test_res_type == 'CE':
            with open(res_file_path + str(i) + '_' + test_res_type + '.txt', 'a') as f:
                f.write(fix_code)
                f.close()
        elif test_res_type == 'TLE' or test_res_type == 'RE' or test_res_type == 'MLE':
            with open(res_file_path + str(i) + '_' + test_res_type + '.txt', 'a') as f:
                f.write(fix_code)
                f.write('\n')
                f.write('input: ' + test_res['input'] + '\n')
                f.write('expect: ' + test_res['expect'] + '\n')
                f.close()
        else:
            with open(res_file_path + str(i) + '_' + test_res_type + '.txt', 'a') as f:
                f.write(fix_code)
                f.write('\n')
                f.write('input: ' + test_res['input'] + '\n')
                f.write('expect: ' + test_res['expect'] + '\n')
                f.write('actual: ' + test_res['actual'] + '\n')
                f.close()

        print(fix_code)
        print(test_res)

        for file_name in listdir('./'):
            if file_name.endswith('.class') or file_name.startswith('Main'):
                os.remove(file_name)

        if test_res_type == 'AC':
            break


# RQ1
def query_only_with_bug():
    count=0
    rq1_res_file=open('rq1_res.csv','r')
    rq1_reader=csv.reader(rq1_res_file)
    rq1_res=[]
    for line in rq1_reader:
        rq1_res.append(line[0])
    rq1_res_file.close()

    for line in islice(reader, count, None):
        if str(count) in rq1_res:
            count+=1
            continue
        bug=line[3]
        query= base_prompt + bug
        test_fix(query,count,line[1])
        count+=1


# RQ2
def query_with_problem():
    count=0
    rq1_res_file=open('rq1_res.csv','r')
    rq1_reader=csv.reader(rq1_res_file)
    rq1_res=[]
    for line in rq1_reader:
        rq1_res.append(line[0])
    rq1_res_file.close()

    rq2_res_file=open('rq2_problem.csv','r')
    rq2_reader=csv.reader(rq2_res_file)
    rq2_res=[]
    for line in rq2_reader:
        rq2_res.append(line[0])
    rq2_res_file.close()
    for line in islice(reader, count, None):
        if str(count) in rq1_res or str(count) in rq2_res:
            count+=1
            continue

        bug=line[3]
        query= base_prompt + bug

        task=line[1]
        contest=task.split('/')[0]
        problem_id=task.split('/')[1]
        path_to_problem='problems/'+contest+'/'+problem_id+'.txt'
        problem_file=open(path_to_problem,'r')
        problem_description=problem_file.read()
        problem_file.close()

        query+='\n\n'
        query+=prompt_problem
        query+=problem_description
        print(query)

        test_fix(query,count,line[1])
        count+=1


def get_200_chars_of_file(file_name):
    file = open(file_name, 'r')
    res=file.read()
    if len(res)>200:
        res=res[0:201]
        res+='...\n'
    # lines = file.readlines()
    # if len(lines) > 20:
    #     lines = lines[0:21]
    # res = ''
    # for line in lines:
    #     res += line
    return res


def get_200_chars(str):
    if len(str)>200:
        str=str[0:201]
        str+='...\n'
    return str


def get_bug_type_prompt(bug_type):
    res=''
    if bug_type=='CE':
        res=prompt_ce
    elif bug_type=='TLE':
        res=prompt_tle
    elif bug_type=='RE':
        res=prompt_re
    elif bug_type=='MLE':
        res=prompt_mle
    else:
        res=prompt_wa
    return res


def query_with_error_info():
    rq1_res_file=open('rq1_res.csv','r')
    rq1_reader=csv.reader(rq1_res_file)
    rq1_res=[]
    for line in rq1_reader:
        rq1_res.append(line[0])
    rq1_res_file.close()

    rq2_res_file=open('rq2_location.csv','r')
    rq2_reader=csv.reader(rq2_res_file)
    rq2_res=[]
    for line in rq2_reader:
        rq2_res.append(line[0])
    rq2_res_file.close()

    count=0
    for line in islice(reader, count, None):
        if str(count) in rq1_res or str(count) in rq2_res:
            count+=1
            continue

        bug=line[3]
        query= base_prompt + bug+'\n\n'

        bug_type=line[5]
        if bug_type=='CE':
            query+=prompt_ce
        elif bug_type=='TLE' or bug_type=='RE' or bug_type=='MLE':
            if bug_type=='TLE':
                query+=prompt_tle
            elif bug_type=='RE':
                query+=prompt_re
            else:
                query+=prompt_mle

            query+=get_200_chars_of_file('error_info/' + str(count) + '/input.txt')

            query+='\n'
            query+=prompt_expect
            query+=get_200_chars_of_file('error_info/' + str(count) + '/expect.txt')
        elif bug_type=='WA':
            query+=prompt_wa
            query+=get_200_chars_of_file('error_info/' + str(count) + '/input.txt')
            query+='\n'
            query+=prompt_expect
            query+=get_200_chars_of_file('error_info/' + str(count) + '/expect.txt')
            query+='\n'
            query+=prompt_actual
            query+=get_200_chars_of_file('error_info/' + str(count) + '/actual.txt')

        print(query)
        test_fix(query,count,line[1])
        count+=1


def query_with_bug_location():
    rq1_res_file=open('rq1_res.csv','r')
    rq1_reader=csv.reader(rq1_res_file)
    rq1_res=[]
    for line in rq1_reader:
        rq1_res.append(line[0])
    rq1_res_file.close()

    rq2_res_file=open('rq2_location.csv','r')
    rq2_reader=csv.reader(rq2_res_file)
    rq2_res=[]
    for line in rq2_reader:
        rq2_res.append(line[0])
    rq2_res_file.close()

    count=0
    for line in islice(reader, count, None):
        if str(count) in rq1_res or str(count) in rq2_res:
            count+=1
            continue

        bug=line[3]
        query=prompt_location+bug
        print(query)
        test_fix(query,count,line[1])
        count+=1


def get_gpt_response(messages):
    success = False
    while not success:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            success = True
        except Exception as e:
            print(e)
            if "This model's maximum context length is 4097 tokens." in str(e):
                return -1
            continue
    response = completion['choices'][0]['message']['content']
    return response


def get_code_from_code_block(str):
    flag = False
    code = ''
    for line in str.split('\n'):
        if not flag:
            if line.startswith('```'):
                flag = True
            continue
        else:
            if line.startswith('```'):
                break
            code += line
            code += '\n'
    return code


# rq3
def perform_more_dialogues():
    rq1_res_file=open('rq1_res.csv','r')
    rq1_reader=csv.reader(rq1_res_file)
    rq1_res=[]
    for line in rq1_reader:
        rq1_res.append(line[0])
    rq1_res_file.close()

    rq2_res_file=open('rq2_error_info_res.csv','r')
    rq2_reader=csv.reader(rq2_res_file)
    rq2_res=[]
    for line in rq2_reader:
        rq2_res.append(line[0])
    rq2_res_file.close()

    count=0
    for line in islice(reader, count, None):
        if str(count) in rq1_res or str(count) in rq2_res:
            count+=1
            continue
            
        bug=line[3]
        query= base_prompt + bug+'\n\n'

        bug_type=line[5]
        query+=get_bug_type_prompt(bug_type)
        if bug_type=='TLE' or bug_type=='RE' or bug_type=='MLE':
            query+=get_200_chars_of_file('error_info/' + str(count) + '/input.txt')
            query+='\n'
            query+=prompt_expect
            query+=get_200_chars_of_file('error_info/' + str(count) + '/expect.txt')
        elif bug_type=='WA':
            query+=get_200_chars_of_file('error_info/' + str(count) + '/input.txt')
            query+='\n'
            query+=prompt_expect
            query+=get_200_chars_of_file('error_info/' + str(count) + '/expect.txt')
            query+='\n'
            query+=prompt_actual
            query+=get_200_chars_of_file('error_info/' + str(count) + '/actual.txt')
        # query+='\n\n'
        # query+=prompt_fix_again

        print(query)
        messages = [
            {"role": "user", "content": query}
        ]
        response=get_gpt_response(messages)
        fix_code=get_code_from_code_block(response)
        test_res = run_test_case(fix_code, line[1], 1024)
        for file_name in listdir('./'):
            if file_name.endswith('.class') or file_name.startswith('Main'):
                os.remove(file_name)
        os.mkdir('results_RQ3/results_RQ3_12/'+str(count))
        with open('results_RQ3/results_RQ3_12/'+str(count)+'/'+'0'+'_'+test_res['res']+'.txt','a') as f:
            f.write(fix_code)
        if test_res['res']!='AC':
            for i in range(1,5):
                messages.append({"role":"assistant","content":response})
                new_query=''
                new_bug_type=test_res['res']
                if new_bug_type=='TLE' or new_bug_type=='RE' or new_bug_type=='MLE':
                    if new_bug_type=='TLE':
                        new_query+=prompt_still_tle
                    elif new_bug_type=='RE':
                        new_query+=prompt_still_re
                    else:
                        new_query+=prompt_still_mle
                    new_query += get_200_chars(test_res['input'])
                    new_query += '\n'
                    new_query += prompt_expect
                    new_query += get_200_chars(test_res['expect'])
                elif new_bug_type=='CE':
                    new_query+=prompt_still_ce
                else:
                    new_query+=prompt_still_wa
                    new_query += get_200_chars(test_res['input'])
                    new_query += '\n'
                    new_query += prompt_expect
                    new_query += get_200_chars(test_res['expect'])
                    new_query += '\n'
                    new_query += prompt_actual
                    new_query += get_200_chars(test_res['actual'])
                new_query+='\n\n'
                new_query+=prompt_fix_again
                print(new_query)
                messages.append({"role":"user","content":new_query})
                print(messages)
                response=get_gpt_response(messages)
                while response==-1:
                    del messages[2]
                    del messages[2]
                    response=get_gpt_response(messages)
                fix_code=get_code_from_code_block(response)
                test_res=run_test_case(fix_code,line[1],1024)
                for file_name in listdir('./'):
                    if file_name.endswith('.class') or file_name.startswith('Main'):
                        os.remove(file_name)
                with open('results_RQ3/results_RQ3_12/'+str(count)+'/'+str(i)+'_'+test_res['res']+'.txt','a') as f:
                    f.write(fix_code)
                if test_res['res']=='AC':
                    break
        count+=1


def rq4():
    contest='abc297'
    # for contest in listdir('problems'):
    #     if contest[0]=='.':
    #         continue
    # for problem in listdir('problems/'+contest):
    problem='Ex'
    problem_path='problems/'+contest+'/'+problem+'.txt'
    problem_text=''
    with open(problem_path,'r') as f:
        problem_text=f.read()
        f.close()

    query="Use Java to solve the following problem. The class name must be 'Main'. return the code in the form of markdown code block.\n"
    query+=problem_text
    query+='\n'
    query+='The test cases are:\n'

    test_case_path='AtCoderTestCasesOfficial/'+contest+'/'+problem+'/'
    test_case_in=os.listdir(test_case_path+'in')
    test_case_out=os.listdir(test_case_path+'out')
    for i in range(0,len(test_case_in)):
        input_file=test_case_in[i]
        output_file=test_case_out[i]
        with open(test_case_path+'in/'+input_file,'r') as f:
            case_input=f.read()
        with open(test_case_path+'out/'+output_file,'r') as f:
            case_output=f.read()
        query+="input: "+case_input
        query+="output: "+case_output
        query+='\n'
    print(query)

    messages = [
        {"role": "user", "content": query}
    ]
    response = get_gpt_response(messages)
    generated_code = get_code_from_code_block(response)
    print(generated_code)
    print(contest+'/'+problem)
    test_res = run_test_case(generated_code, contest+'/'+problem, 1024)
    print(test_res['res'])
    for file_name in listdir('./'):
        if file_name.endswith('.class') or file_name.startswith('Main'):
            os.remove(file_name)

    with open('results_RQ4_4/'+contest+'/'+problem+'/0_'+test_res['res']+'.txt','w') as f:
        f.write(generated_code)
    if test_res['res']=='AC':
        # continue
        return
    for i in range(1,31):
        messages.append({"role":"assistant","content":response})
        new_query=''
        new_bug_type=test_res['res']
        if new_bug_type=='TLE' or new_bug_type=='RE' or new_bug_type=='MLE':
            if new_bug_type=='TLE':
                new_query+=prompt_still_tle
            elif new_bug_type=='RE':
                new_query+=prompt_still_re
            else:
                new_query+=prompt_still_mle
            new_query += get_200_chars(test_res['input'])
            new_query += '\n'
            new_query += prompt_expect
            new_query += get_200_chars(test_res['expect'])
        elif new_bug_type=='CE':
            new_query+=prompt_still_ce
        else:
            new_query+=prompt_still_wa
            new_query += get_200_chars(test_res['input'])
            new_query += '\n'
            new_query += prompt_expect
            new_query += get_200_chars(test_res['expect'])
            new_query += '\n'
            new_query += prompt_actual
            new_query += get_200_chars(test_res['actual'])
        new_query+='\n\n'
        new_query+=prompt_fix_again
        print(new_query)
        messages.append({"role":"user","content":new_query})
        print(messages)
        response=get_gpt_response(messages)
        while response==-1:
            del messages[2]
            del messages[2]
            response=get_gpt_response(messages)
        fix_code=get_code_from_code_block(response)
        test_res=run_test_case(fix_code,contest+'/'+problem,1024)
        for file_name in listdir('./'):
            if file_name.endswith('.class') or file_name.startswith('Main'):
                os.remove(file_name)
        with open('results_RQ4_4/'+contest+'/'+problem+'/'+str(i)+'_'+test_res['res']+'.txt','a') as f:
            f.write(fix_code)
        if test_res['res']=='AC':
            break


def generate_solution_for_problems():
    for contest in listdir('problems'):
        if contest[0]=='.':
            continue
        for problem in listdir('problems/'+contest):
            problem_path='problems/'+contest+'/'+problem[0:-4]+'.txt'
            problem_text=''
            with open(problem_path,'r') as f:
                problem_text=f.read()
                f.close()

            query = "Use Java to solve the following problem. The class name must be 'Main'. return the code in the form of markdown code block.\n"
            query += problem_text

            messages = [
                {"role": "user", "content": query}
            ]

            for i in range(0,10):
                response = get_gpt_response(messages)
                generated_code = get_code_from_code_block(response)
                print(generated_code)
                with open('initial_problem_solutions/'+contest+'/'+problem[0:-4]+'/'+str(i)+'.txt','w') as f:
                    f.write(generated_code)


def self_repair():
    for contest in os.listdir('gpt_solutions'):
        for problem in os.listdir('gpt_solutions/'+contest):
            path='gpt_solutions/'+contest+'/'+problem
            bug=''
            with open(path,'r') as f:
                bug=f.read()

            query = base_prompt + bug + '\n\n'

            task=contest+'/'+problem[0:-4]
            bug_test_res=run_test_case(bug,task,1024)

            if bug_test_res['res']=='AC':
                continue

            bug_type=bug_test_res['res']
            query += get_bug_type_prompt(bug_type)
            if bug_type == 'TLE' or bug_type == 'RE' or bug_type == 'MLE':
                query += get_200_chars(bug_test_res['input'])
                query += '\n'
                query += prompt_expect
                query += get_200_chars(bug_test_res['expect'])
            elif bug_type == 'WA':
                query += get_200_chars(bug_test_res['input'])
                query += '\n'
                query += prompt_expect
                query += get_200_chars(bug_test_res['expect'])
                query += '\n'
                query += prompt_actual
                query += get_200_chars(bug_test_res['actual'])
            # query+='\n\n'
            # query+=prompt_fix_again

            print(query)
            messages = [
                {"role": "user", "content": query}
            ]
            response = get_gpt_response(messages)
            fix_code = get_code_from_code_block(response)
            test_res = run_test_case(fix_code, task, 1024)
            for file_name in listdir('./'):
                if file_name.endswith('.class') or file_name.startswith('Main'):
                    os.remove(file_name)

            with open('results_RQ4_final/'+contest+'/'+problem[0:-4]+'/0_'+test_res['res']+'.txt','w') as f:
                f.write(fix_code)

            if test_res['res'] != 'AC':
                for i in range(1, 30):
                    messages.append({"role": "assistant", "content": response})
                    new_query = ''
                    new_bug_type = test_res['res']
                    if new_bug_type == 'TLE' or new_bug_type == 'RE' or new_bug_type == 'MLE':
                        if new_bug_type == 'TLE':
                            new_query += prompt_still_tle
                        elif new_bug_type == 'RE':
                            new_query += prompt_still_re
                        else:
                            new_query += prompt_still_mle
                        new_query += get_200_chars(test_res['input'])
                        new_query += '\n'
                        new_query += prompt_expect
                        new_query += get_200_chars(test_res['expect'])
                    elif new_bug_type == 'CE':
                        new_query += prompt_still_ce
                    else:
                        new_query += prompt_still_wa
                        new_query += get_200_chars(test_res['input'])
                        new_query += '\n'
                        new_query += prompt_expect
                        new_query += get_200_chars(test_res['expect'])
                        new_query += '\n'
                        new_query += prompt_actual
                        new_query += get_200_chars(test_res['actual'])
                    new_query += '\n\n'
                    new_query += prompt_fix_again
                    print(new_query)
                    messages.append({"role": "user", "content": new_query})
                    print(messages)
                    response = get_gpt_response(messages)
                    while response == -1:
                        del messages[2]
                        del messages[2]
                        response = get_gpt_response(messages)
                    fix_code = get_code_from_code_block(response)
                    test_res = run_test_case(fix_code, task, 1024)
                    for file_name in listdir('./'):
                        if file_name.endswith('.class') or file_name.startswith('Main'):
                            os.remove(file_name)
                    with open('results_RQ4_final/'+contest+'/'+problem[0:-4]+'/'+str(i)+'_'+test_res['res']+'.txt','w') as f:
                        f.write(fix_code)
                    if test_res['res'] == 'AC':
                        break




if __name__ == '__main__':
    self_repair()


#     code="""
# import java.util.Scanner;
#
# public class Main {
#     public static void main(String[] args) {
#         Scanner scanner = new Scanner(System.in);
#         String S = scanner.next();
#
#         int countR = 0;
#         int countB = 0;
#         int countN = 0;
#         int countK = 0;
#         int x = -1, y = -1, z = -1;
#
#         for (int i = 0; i < S.length(); i++) {
#             char c = S.charAt(i);
#
#             if (c == 'R') {
#                 countR++;
#                 if (x == -1) x = i;
#                 else if (y == -1) y = i;
#             } else if (c == 'B') {
#                 countB++;
#             } else if (c == 'N') {
#                 countN++;
#             } else if (c == 'K') {
#                 countK++;
#                 z = i;
#             }
#         }
#
#         if (countR != 2 || countB != 2 || countN != 2 || countK != 1) {
#             System.out.println("No");
#             return;
#         }
#
#         if ((x % 2 == 0 && y % 2 == 0) || (x % 2 == 1 && y % 2 == 1)) {
#             System.out.println("No");
#             return;
#         }
#
#         if (!(x < z && z < y)) {
#             System.out.println("No");
#             return;
#         }
#
#         System.out.println("Yes");
#     }
# }
#
#     """
#     problem="""
# There are N piles of stones. Initially, the i-th pile contains Ai stones. With these piles, Taro the First and Jiro the Second play a game against each other.
# Taro the First and Jiro the Second make the following move alternately, with Taro the First going first:
# •Choose a pile of stones, and remove between L and R stones (inclusive) from it.
# A player who is unable to make a move loses, and the other player wins. Who wins if they optimally play to win?
#     """
#     query=base_prompt+code
#     print(query)
#     fixed=get_fix_from_gpt(query)
#     print(run_test_case(fixed,'abc297/B',1024))


from run_testcase import run_test_case
from run_testcase import run_all_test_case
from os import listdir
import os


def run_all_testcases():
    for contest in listdir('initial_problem_solutions'):
        for problem in listdir('initial_problem_solutions/'+contest):
            solution_pass_most_cases=''
            max_passed_cases_num=-1

            for i in range(0,10):
                file_path='initial_problem_solutions/'+contest+'/'+problem+'/'+str(i)+'.txt'
                code=''
                with open(file_path,'r',encoding='utf-8') as f:
                    code=f.read()
                problem_id=contest+'/'+problem
                test_res=run_all_test_case(code,problem_id,1024)

                print(code)
                print(problem_id)

                passed_num=0
                for case_res in test_res:
                    if case_res['res']=='AC':
                        passed_num+=1

                if passed_num>max_passed_cases_num:
                    solution_pass_most_cases=code
                    max_passed_cases_num=passed_num

            with open('gpt_solutions/'+contest+'/'+problem+'.txt','w') as f:
                f.write(solution_pass_most_cases)




if __name__=='__main__':
    run_all_testcases()

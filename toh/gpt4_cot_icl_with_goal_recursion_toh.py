import openai
from gen_start_config import *
# from toh_twoshot_cot_examples import standard_prompt
import time
import argparse
import os

from openai import AzureOpenAI

all_As, all_Bs, all_Cs = generate_all_start_config()

number_message_mapping = {3:"three numbers -- 0, 1, and 2 --", 4:"four numbers -- 0, 1, 2, and 3 --",5:"five numbers -- 0, 1, 2, 3, and 4 --"}
number_target_mapping = {3:"C = [0, 1, 2]", 4:"C = [0, 1, 2, 3]",5:"C = [0, 1, 2, 3, 4]"}
num_steps = {3:"10",4:"20"}

def check_path(path):
	if not os.path.exists(path):
		os.mkdir(path)

parser = argparse.ArgumentParser()

parser.add_argument

parser.add_argument('--output_dir',type=str, help='directory name where output log files will be stored', required= True)

args = parser.parse_args()
print(args)



icl_examples = [ 3, 22]
#

for i in range(26):
	if (i+1) not in icl_examples:
		start_time = time.time()
		A=all_As[i] 

		B=all_Bs[i]

		C=all_Cs[i]
		num_disks = max(A+B+C)+1
		prompt = """Consider the following puzzle problem:

		Problem description:
		- There are three lists labeled A, B, and C.
		- There is a set of numbers distributed among those three lists.
		- You can only move numbers from the rightmost end of one list to the rightmost end of another list.
		Rule #1: You can only move a number if it is at the rightmost end of its current list.
		Rule #2: You can only move a number to the rightmost end of a list if it is larger than the other numbers in that list.

		A move is valid if it satisfies both Rule #1 and Rule #2.
		A move is invalid if it violates either Rule #1 or Rule #2.


		Goal: The goal is to end up in the goal configuration where all numbers are in list C, in ascending order using minimum number of moves.

		Using the goal recursion strategy, a subgoal can be generated from the starting configuration that helps in reaching the goal configuration using minimum number of moves. First if the smallest number isn't at the correct position in list C, then set the subgoal of moving the smallest number to its correct position in list C.
		But before that, the numbers larger than the smallest number and present in the same list as the smallest number must be moved to a list other than list C. 
		This subgoal is recursive because in order to move the next smallest number to the list other than list C, the numbers larger than the next smallest number and present in the same list as the next smallest number must be moved to a list different from the previous other list and so on.
		Note in the subgoal configuration all numbers should always be in ascending order in all the three lists.
		


		Here are two examples:
		

		Example 1:

		This is the starting configuration:
		A = [0, 1]
		B = [2]
		C = []
		This is the goal configuration:
		A = []
		B = []
		C = [0, 1, 2]

		I need to move 0 from list A to list C. 
		Step 1. Find the numbers to the right of 0 in list A. There is 1 to the right of 0.
		Step 2. Find the numbers larger than 0 in list C. There are none.
		I will move the numbers found in Step 1 and Step 2 to list B. Hence I will move 1 from list A to list B. Also numbers should be in ascending order in list B.
		Subgoal:
		A = [0]
		B = [1, 2]
		C = []
		
		Here is the sequence of minimum number of moves along with reasoning for each move to reach the subgoal configuration from the starting configuration:

		I need to move 0 from A to C. But before that I need to move the number present to the right of 0, which is 1 to B. There is a number larger than 1 already present in list B. Hence I first need to move 2 from B to C.
		Move 2 from B to C.
		A = [0, 1]
		B = []
		C = [2]

		I need to move 0 from A to C. But before that I need to move the number present to the right of 0, which is 1 to B.
		Move 1 from A to B.
		A = [0]
		B = [1]
		C = [2]

		I need to move 0 from A to C. There is a number larger than 0 already present in list C. Hence I first need to move 2 from C to B.
		Move 2 from C to B.
		A = [0]
		B = [1, 2]
		C = []

		Here is the sequence of minimum number of moves along with reasoning for each move to reach the goal configuration from the subgoal configuration:

		There is no number to the right of 0 in A, and there is no number larger than 0 in C. Hence, I can move 0 from A to C.
		Move 0 from A to C.
		A = []
		B = [1, 2]
		C = [0]

		I need to move 1 from B to C. But before that I need to move the number present to the right of 1, which is 2 to A.
		Move 2 from B to A.
		A = [2]
		B = [1]
		C = [0]

		There is no number to the right of 1 in B, and there is no number larger than 1 in C. Hence, I can move 1 from B to C.
		Move 1 from B to C.
		A = [2]
		B = []
		C = [0, 1]

		There is no number to the right of 2 in A, and there is no number larger than 2 in C. Hence, I can move 2 from A to C.
		Move 2 from A to C.
		A = []
		B = []
		C = [0, 1, 2]
		

		Example 2:

		This is the starting configuration:
		A = [1]
		B = [0]
		C = [2]
		This is the goal configuration:
		A = []
		B = []
		C = [0, 1, 2]

		I need to move 0 from list B to list C. 
		Step 1. Find the numbers to the right of 0 in list B. There are none.
		Step 2. Find the numbers larger than 0 in list C. There is 2 which is larger than 0.
		I will move the numbers found in Step 1 and Step 2 to list A. Hence, I will move 2 from list C to list A. Also numbers should be in ascending order in list A.
		Subgoal:
		A = [1, 2]
		B = [0]
		C = []    


		Here is the sequence of minimum number of moves along with reasoning for each move to reach the subgoal configuration from the starting configuration:

		I need to move 0 from B to C. There is a number larger than 0 already present in list C. Hence I first need to move 2 from C to A.
		Move 2 from C to A.
		A = [1, 2]
		B = [0]
		C = []

		Here is the sequence of minimum number of moves along with reasoning for each move to reach the goal configuration from the subgoal configuration:

		There is no number to the right of 0 in B, and there is no number larger than 0 in C. Hence, I can move 0 from B to C.
		Move 0 from B to C.
		A = [1, 2]
		B = []
		C = [0]

		I need to move 1 from A to C. But before that I need to move the number present to the right of 1, which is 2 to B.
		Move 2 from A to B.
		A = [1]
		B = [2]
		C = [0]

		There is no number to the right of 1 in A, and there is no number larger than 1 in C. Hence, I can move 1 from A to C.
		Move 1 from A to C.
		A = []
		B = [2]
		C = [0, 1]

		There is no number to the right of 2 in B, and there is no number larger than 2 in C. Hence, I can move 2 from B to C.
		Move 2 from B to C.
		A = []
		B = []
		C = [0, 1, 2]


		Here is the task:
		
		This is the starting configuration:
		{}
		{}
		{}
		This is the goal configuration:
		A = []
		B = []
		{}
		
		
		First generate a single subgoal from the starting configuration, that helps in reaching the goal configuration using minimum number of moves. Then give me the sequence of moves along with reasoning for each move to solve the puzzle using the subgoal configuration from the starting configuration, updating the lists after each move. Please try to use as few moves as possible, and make sure to follow the rules listed above. Please limit your answer to a maximum of {} steps.
	
		
		""".format("A = "+str(A),"B = "+str(B),"C = "+str(C),number_target_mapping[num_disks],num_steps[num_disks])

		
		test_dir = './logs/'
		check_path(test_dir)
		output_dir = test_dir + args.output_dir + '/'
		check_path(output_dir)

		with open(output_dir+'problem{}.log'.format(i+1), 'a') as w:
			w.write(prompt +'\n')

		


		input = [{
		    "role": "system",
		    "content": "you are an AI assistant",
		}]

		input.append({
		    "role": "user",
		    "content": prompt,
		})

		another_cur_try = 0
		while another_cur_try <10:
			try:
				time1 = time.time()
				response = client.chat.completions.create(model=deployment_name, messages=input,temperature=0.0, top_p= 0 ,max_tokens=4000)
			

				time2 = time.time()
				

				break

			except Exception as e:
				err = f"Error: {str(e)}"
				print(err)
				time.sleep(120)
				another_cur_try+=1
				
				continue


		with open(output_dir+'problem{}.log'.format(i+1), 'a') as w:
			w.write("GPT-4 Response>>>>>>>\n"+response.choices[0].message.content)
		
		
		
		
		end_time = time.time()

		
		print("done solving problem {}".format(i+1))

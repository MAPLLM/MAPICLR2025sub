import openai
from gen_start_config import *
import time
import os
import argparse
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



for i in range(26):
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

	Goal: The goal is to end up in the configuration where all numbers are in list C, in ascending order using minimum number of moves.
	
	This is the starting configuration:
	{}
	{}
	{}
	This is the goal configuration:
	A = []
	B = []
	{}
	
	Using the goal recursion strategy, generate a subgoal from the starting configuration that helps in reaching the goal configuration using minimum number of moves. First if the smallest number isn't at the correct position in list C, then set the subgoal of moving the smallest number to its correct position in list C.
	But before that, the numbers larger than the smallest number and present in the same list as the smallest number must be moved to a list other than list C. 
	This subgoal is recursive because in order to move the next smallest number to the list other than list C, the numbers larger than the next smallest number and present in the same list as the next smallest number must be moved to a list different from the previous other list and so on.
	Note in the subgoal configuration all numbers should always be in ascending order in all the three lists.

	First generate a single subgoal from the starting configuration, that helps in reaching the goal configuration using minimum number of moves. Then give me the sequence of moves to solve the puzzle using the subgoal configuration from the starting configuration, updating the lists after each move. Please try to use as few moves as possible, and make sure to follow the rules listed above. Please limit your answer to a maximum of {} steps.
	

	""".format("A = "+str(A),"B = "+str(B),"C = "+str(C),number_target_mapping[num_disks],num_steps[num_disks])

# Please format your answer as below:
# 	Step 1. Move <N> from list <src> to list <tgt>.
# 	A = []
# 	B = []
# 	C = []
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
	while another_cur_try <5:
		try:
			response = client.chat.completions.create(model=deployment_name, messages=input,temperature=0.0, top_p= 0 ,max_tokens=4000)
			

			# num_input_tokens= response["usage"]["prompt_tokens"]
			# num_output_tokens= response["usage"]["completion_tokens"]

			break

		except Exception as e:
			err = f"Error: {str(e)}"
			print(err)
			time.sleep(60)
			another_cur_try+=1
			
			continue

	


	with open(output_dir+'problem{}.log'.format(i+1), 'a') as w:
		w.write("GPT-4 Response>>>>>>>\n"+response.choices[0].message.content)
	
	# with open(output_dir+'problem{}.log'.format(i+1), 'a') as w:
	# 	w.write("\n\n Number of input tokens = {} \n Number of output tokens = {}".format(num_input_tokens,num_output_tokens))
	
	print("done solving problem {}".format(i+1))

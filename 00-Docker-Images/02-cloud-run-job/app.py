import os

def main():
    task_index = os.getenv('CLOUD_RUN_TASK_INDEX')
    task_count = os.getenv('CLOUD_RUN_TASK_COUNT')
 
    print(f'CLOUD_RUN_TASK_INDEX: {task_index}')
    print(f'CLOUD_RUN_TASK_COUNT: {task_count}')


if __name__ == '__main__':
    main()
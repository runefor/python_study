#%%
import time
import threading        # 멀티스레딩을 위한 모듈
import multiprocessing  # 멀티프로세싱을 위한 모듈
import os               # CPU 코어 수를 확인하기 위한 모듈
import random           # I/O 작업 시뮬레이션을 위한 랜덤 시간 생성

print(f"이 Colab 환경의 CPU 코어 수: {os.cpu_count()}")

# 실행할 작업의 수 (CPU 코어 수와 비슷하게 설정하면 비교하기 좋습니다)
NUM_TASKS = os.cpu_count() if os.cpu_count() else 2 # Colab에서 코어 수 반환 안될 경우 대비

#%%

# --- 1. I/O 바운드 작업 (대기 시뮬레이션) ---
def io_bound_task(task_id):
    """
    네트워크 요청이나 파일 읽기/쓰기처럼
    대기 시간이 긴 작업을 시뮬레이션합니다.
    """
    # 0.5초에서 1.0초 사이의 랜덤한 시간 동안 대기
    wait_time = random.uniform(0.5, 1.0)
    print(f"[I/O 작업 {task_id}] 시작 - {wait_time:.2f}초 동안 대기...")
    time.sleep(wait_time) # time.sleep()으로 대기 상태를 만듭니다.
    print(f"[I/O 작업 {task_id}] 완료!")

# --- 2. CPU 바운드 작업 (계산 시뮬레이션) ---
def cpu_bound_task(task_id):
    """
    복잡한 수학 계산처럼 CPU를 많이 사용하는 작업을 시뮬레이션합니다.
    """
    print(f"[CPU 작업 {task_id}] 시작 - 계산 중...")
    # 간단한 계산을 많이 반복하여 CPU 사용
    count = 0
    # 약 0.5초 동안 계산 반복 (시간은 조절 가능)
    end_time = time.time() + 0.5
    while time.time() < end_time:
        count += 1 # 간단한 연산 반복
    print(f"[CPU 작업 {task_id}] 완료 (반복 {count}회)")

# --- 실행 시간 측정 및 비교를 위한 함수들 ---

# 1. 순차 실행 함수
def run_sequentially(task_function, num_tasks):
    print(f"\n--- {task_function.__name__} 순차 실행 ({num_tasks}개 작업) ---")
    start_time = time.time()
    for i in range(num_tasks):
        task_function(i) # 작업을 하나씩 순서대로 실행
    end_time = time.time()
    duration = end_time - start_time
    print(f"--- 순차 실행 완료 ---")
    print(f"총 소요 시간: {duration:.4f} 초")
    return duration

# 2. 멀티스레딩 실행 함수
def run_with_threading(task_function, num_tasks):
    print(f"\n--- {task_function.__name__} 멀티스레딩 실행 ({num_tasks}개 스레드) ---")
    threads = []
    start_time = time.time()
    # 스레드 생성 및 시작
    for i in range(num_tasks):
        thread = threading.Thread(target=task_function, args=(i,))
        threads.append(thread)
        thread.start() # 스레드 실행 시작
    # 모든 스레드가 끝날 때까지 기다림
    for thread in threads:
        thread.join()
    end_time = time.time()
    duration = end_time - start_time
    print(f"--- 멀티스레딩 실행 완료 ---")
    print(f"총 소요 시간: {duration:.4f} 초")
    return duration

# 3. 멀티프로세싱 실행 함수
def run_with_multiprocessing(task_function, num_tasks):
    # 중요: Colab이나 특정 환경에서는 multiprocessing 사용 시
    #       if __name__ == '__main__': 구문이 필요할 수 있으나,
    #       노트북 셀에서는 보통 없어도 동작합니다.
    print(f"\n--- {task_function.__name__} 멀티프로세싱 실행 ({num_tasks}개 프로세스) ---")
    processes = []
    start_time = time.time()
    # 프로세스 생성 및 시작
    for i in range(num_tasks):
        process = multiprocessing.Process(target=task_function, args=(i,))
        processes.append(process)
        process.start() # 프로세스 실행 시작
    # 모든 프로세스가 끝날 때까지 기다림
    for process in processes:
        process.join()
    end_time = time.time()
    duration = end_time - start_time
    print(f"--- 멀티프로세싱 실행 완료 ---")
    print(f"총 소요 시간: {duration:.4f} 초")
    return duration

print("="*20, "I/O 바운드 작업 테스트", "="*20)

if __name__ == "__main__":

    # 1. I/O 작업을 순차적으로 실행
    seq_io_time = run_sequentially(io_bound_task, NUM_TASKS)

    # 2. I/O 작업을 멀티스레딩으로 실행
    thread_io_time = run_with_threading(io_bound_task, NUM_TASKS)

    # 3. I/O 작업을 멀티프로세싱으로 실행 (참고용)
    #    (I/O 작업에는 스레딩보다 오버헤드가 클 수 있음)
    process_io_time = run_with_multiprocessing(io_bound_task, NUM_TASKS)

    print("\n--- I/O 작업 결과 요약 ---")
    print(f"순차 실행 시간: {seq_io_time:.4f} 초")
    print(f"스레딩 실행 시간: {thread_io_time:.4f} 초")
    print(f"프로세싱 실행 시간: {process_io_time:.4f} 초")
    print("\n결론: I/O 바운드 작업은 스레드가 대기하는 동안 다른 스레드가 실행될 수 있으므로,")
    print("      멀티스레딩이 순차 실행보다 훨씬 빠릅니다.")
    print("      (멀티프로세싱도 가능하지만, 스레딩보다 오버헤드가 커서 덜 효율적일 수 있습니다.)")

    print("\n\n", "="*20, "CPU 바운드 작업 테스트", "="*20)

    # 1. CPU 작업을 순차적으로 실행
    seq_cpu_time = run_sequentially(cpu_bound_task, NUM_TASKS)

    # 2. CPU 작업을 멀티스레딩으로 실행
    thread_cpu_time = run_with_threading(cpu_bound_task, NUM_TASKS)

    # 3. CPU 작업을 멀티프로세싱으로 실행
    process_cpu_time = run_with_multiprocessing(cpu_bound_task, NUM_TASKS)

    print("\n--- CPU 작업 결과 요약 ---")
    print(f"순차 실행 시간: {seq_cpu_time:.4f} 초")
    print(f"스레딩 실행 시간: {thread_cpu_time:.4f} 초")
    print(f"프로세싱 실행 시간: {process_cpu_time:.4f} 초")
    print("\n결론: CPU 바운드 작업은 파이썬의 GIL 때문에 멀티스레딩으로 속도 향상을 보기 어렵습니다.")
    print("      오히려 스레드 전환 비용 때문에 순차 실행보다 느릴 수도 있습니다.")
    print("      반면, 멀티프로세싱은 여러 CPU 코어를 동시에 활용하므로 순차 실행보다 훨씬 빠릅니다.")
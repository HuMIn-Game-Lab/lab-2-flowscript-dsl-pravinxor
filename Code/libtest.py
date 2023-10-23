#!/usr/bin/env python

from ctypes import cdll, POINTER, c_char, string_at
import json

lib = cdll.LoadLibrary('./Code/job_system/target/debug/libjobsystem.so')

lib.create_jobsystem.restype = POINTER(c_char)
lib.add_worker.restype = POINTER(c_char)
lib.get_job.restype = POINTER(c_char)
lib.send_job.restype = POINTER(c_char)

def call_ffi(func, payload=None):
    print(f"Calling FFI function: {func.__name__}...")
    if payload:
        res_ptr = func(payload.encode('utf-8'))
    else:
        res_ptr = func()
    json_str = json.loads(string_at(res_ptr).decode('utf-8'))
    lib.free_str(res_ptr)
    return json_str

def create_jobsystem():
    return call_ffi(lib.create_jobsystem)

def add_worker(system_id):
    payload = json.dumps({"system_id": system_id})
    return call_ffi(lib.add_worker, payload)

def send_job(system_id, job_type, input_data=None):
    payload = json.dumps({
        "system_id": system_id,
        "type": job_type,
        "input": input_data
    })
    return call_ffi(lib.send_job, payload)

def get_job(handle_id):
    payload = json.dumps({"handle_id": handle_id})
    return call_ffi(lib.get_job, payload)

# Usage example
if __name__ == '__main__':
    system_info = create_jobsystem()
    print(f"Created JobSystem: {system_info}")

    worker_info = add_worker(system_info['system_id'])
    print(f"Added Worker: {worker_info}")

    job_info = send_job(system_info['system_id'], 'make', {'target': 'demo'})
    print(f"Sent Job: {job_info}")

    result_info = get_job(job_info['handle_id'])
    print(f"Job Result: {result_info}")


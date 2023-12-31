#!/usr/bin/env python

from ctypes import cdll, POINTER, c_char, string_at
import json

lib = cdll.LoadLibrary('./Code/job_system/target/debug/libjobsystem.so')

lib.create_jobsystem.restype = POINTER(c_char)
lib.destroy_jobsystem.restype = POINTER(c_char)
lib.add_worker.restype = POINTER(c_char)
lib.get_job.restype = POINTER(c_char)
lib.get_job_status.restype = POINTER(c_char)
lib.send_job.restype = POINTER(c_char)
lib.list_job_types.restype = POINTER(c_char)

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

def destroy_jobsystem(system_id):
    payload = json.dumps({"system_id": system_id})
    return call_ffi(lib.destroy_jobsystem, payload)

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

def list_job_types():
    return call_ffi(lib.list_job_types)

def get_job_status(handle_id):
    payload = json.dumps({"handle_id": handle_id})
    return call_ffi(lib.get_job_status, payload)

def get_job(handle_id):
    payload = json.dumps({"handle_id": handle_id})
    return call_ffi(lib.get_job, payload)

# Usage example
if __name__ == '__main__':
    system_info = create_jobsystem()
    print(f"Created JobSystem: {system_info}\n")

    types = list_job_types()
    print(f"Job types {types}")
    
    worker_info = add_worker(system_info['system_id'])
    print(f"Added Worker: {worker_info}\n")

    job_info = send_job(system_info['system_id'], 'make', {'target': 'demo'})
    print(f"Sent Job: {job_info}\n")
    
    status_info = get_job_status(job_info['handle_id'])
    print(f"Job Status: {status_info}\n")

    status_info = get_job(job_info['handle_id'])
    print(f"Job Result: {status_info}\n")

    destroy_status = add_worker(system_info['system_id'])
    print(f"Destroy jobsystem: {destroy_status}")

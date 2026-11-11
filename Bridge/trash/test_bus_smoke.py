#!/usr/bin/env python3
import json
import subprocess
import sys

PROJECT_ROOT = 'c:/Users/crmte/OneDrive/Desktop/Projects/Discovery_Engine'

def post_message(sender, receiver, vector, performative, topic, payload):
    cmd = [
        'python',
        PROJECT_ROOT + '/Bridge/bus_manager.py',
        '--post',
        '--sender', sender,
        '--receiver', receiver,
        '--vector', vector,
        '--performative', performative,
        '--topic', topic,
        '--payload', json.dumps(payload),
    ]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)

def main():
    print('=' * 60)
    print('End-to-End Smoke Test - Bus Manager')
    print('=' * 60)

    # Test 1: Post a task submission
    print('\n[TEST 1] Post task submission (submit_task)')
    payload = {
        'scheme_id': 'TEST_SCHEME_001',
        'title': 'Test Concept Scheme',
        'keywords': ['smoke', 'test'],
        'concepts': [{'name': 'Test_Concept', 'definition': 'A test concept'}],
    }
    result = post_message(
        'aggregator.architect', 'system.master_architect', 'vertical',
        'hypothesis_submission', 'concept_scheme', payload
    )
    print('STDOUT:', result.stdout)
    print('RC:', result.returncode)

    # Test 2: Verify idempotency
    print('\n[TEST 2] SHA256 idempotency test')
    sys.path.insert(0, PROJECT_ROOT + '/Bridge')
    import bus_manager
    key1 = bus_manager.compute_idempotency_key('aggregator.architect', 'TASK1', 'submit_task')
    key2 = bus_manager.compute_idempotency_key('aggregator.architect', 'TASK1', 'submit_task')
    print('Key1:', key1)
    print('Key2:', key2)
    print('Keys match:', key1 == key2)

    print('\n' + '=' * 60)
    print('Smoke Test Complete')
    print('=' * 60)

if __name__ == '__main__':
    main()


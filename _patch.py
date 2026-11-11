p='00_Project_Interface/src/anythingllm_gateway.py'
s=open(p,encoding='utf-8').read()
s=s.replace('ANYTHINGLLM_BASE_URL = "http://127.0.0.1:3001/api/v1"
REQUEST_TIMEOUT = 3
','ANYTHINGLLM_BASE_URL = "http://127.0.0.1:3001/api/v1"
REQUEST_TIMEOUT = 3
ANYTHINGLLM_API_KEY = None
',1)
old='''    url = f"{ANYTHINGLLM_BASE_URL}{path}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
        elif method.upper() == "POST":
            response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)'''
new='''    url = f"{ANYTHINGLLM_BASE_URL}{path}"
    headers = {}
    if ANYTHINGLLM_API_KEY:
        headers["Authorization"] = f"Bearer {ANYTHINGLLM_API_KEY}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        elif method.upper() == "POST":
            response = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)'''
assert old in s, 'block1'
s=s.replace(old,new,1)
old2='''    parser.add_argument(
        "--model",
        default=None,
        help="Optional model name for --send-chat.",
    )
    args = parser.parse_args(argv)'''
new2='''    parser.add_argument(
        "--model",
        default=None,
        help="Optional model name for --send-chat.",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="AnythingLLM API key (Bearer token).",
    )
    args = parser.parse_args(argv)'''
assert old2 in s, 'block2'
s=s.replace(old2,new2,1)
old3='''    if args.test:
        run_test()
        return 0'''
new3='''    global ANYTHINGLLM_API_KEY
    if args.api_key:
        ANYTHINGLLM_API_KEY = args.api_key
    if args.test:
        run_test()
        return 0'''
assert old3 in s, 'block3'
s=s.replace(old3,new3,1)
open(p,'w',encoding='utf-8').write(s)
print('patched')


def build_fun(branch):
    if branch == 'staging':
        print("working on staging auto diployment")
    elif branch == 'main':
        print("working on master auto diployment")
    else:
        print(f"on this {branch} no action!!")

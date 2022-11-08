# PSK Ass Kicker 9000
# Author: Robbie Heine (robbieheine@gmail.com)
# Version: 1.0

from passlib.utils import pbkdf2
import binascii, sys, threading, time

##### Helpful Functions #####

# Computes the psk hash given the ssid and passphrase
def compute_psk(ssid, pwd):
	var = pbkdf2.pbkdf2(str.encode(pwd), str.encode(ssid), 4096, 32)
	return binascii.hexlify(var).decode("utf-8")

##### Thread Classes #####

# Thread that cracks passwords
class Cracked(threading.Thread):
	def __init__(self, threadID, name, counter, s, tpk, p, ai, bi):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.ssid = s
		self.target_psk = tpk
		self.pwds = p
		self.start_index = ai
		self.stop_index = bi
	# Let the cracking begin!
	def run(self):
		print(f'\n~~Thread {self.threadID}~~\nTrying: {self.start_index} -> {self.stop_index}')
		i = self.start_index
		while i < self.stop_index:
			maybe = str(compute_psk(self.ssid, self.pwds[i]))
			if self.target_psk == maybe:
				print(f'Passphrase found!\n{self.target_psk}:{self.ssid} = {self.pwds[i]}')
				break
			i += 1
		print(f'\nThread {self.threadID} Completed')


##### Main #####

# Runs Threads
def run(t, pwds, ssid, psk):
	threads = []
	subdivision = int(len(pwds) / t)
	for i in range(t):
		threads.append(Cracked(i + 1, f'PwdCracker-{i + 1}', i + 1, ssid, psk, pwds, subdivision * i, subdivision * (i + 1)))
		print(f'Thread {i} from {subdivision * i} to {subdivision * (i)}')
		threads[i].start()

# Main
def main():
	print("~~~~~ PSK Ass-Kicker 9000 ~~~~~\n")
	print("SSID >", end=" ")
	ssid = input().strip()
	print("PSK Hash >", end=" ")
	psk = input().strip()
	print("Wordlist >", end=" ")
	w = input().strip()
	print("How many threads? >", end=" ")
	threads = int(input().strip())
	wordlist = open(w, "r", errors="ignore")
	# ssid = "university-guest"
	# psk = "9752f8bc198e546688025be9cb5dd95d61d52e904c8ef2d7babb0cc82376aeda"
	print('\nLoading Wordlist, please be patient...')
	pwds = wordlist.readlines()
	print(f'{len(pwds)} Passwords loaded.')
	run(threads, pwds, ssid, psk)

# Main?
if __name__ == "__main__":
	main()

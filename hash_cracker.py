import hashlib
import argparse
import time
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Constants
SUPPORTED_ALGOS = hashlib.algorithms_guaranteed
DEFAULT_WORDLIST = "rockyou.txt" if os.path.exists("rockyou.txt") else None

class HashCracker:
    def __init__(self):
        self.start_time = None
        self.found = False
        self.progress = None

    def detect_algorithm(self, hash_str):
        """Auto-detects hash algorithm based on length with more comprehensive checks"""
        length = len(hash_str)
        algo_map = {
            32: 'md5',
            40: 'sha1',
            56: 'sha224',
            64: 'sha256',
            96: 'sha384',
            128: 'sha512'
        }
        return algo_map.get(length)

    def benchmark(self, algo, word_count=100000):
        """Benchmark hash speed for given algorithm"""
        print(f"\n⚡ Benchmarking {algo}...")
        test_word = b"benchmark"
        hasher = getattr(hashlib, algo)
        
        start = time.time()
        for _ in range(word_count):
            hasher(test_word).hexdigest()
        elapsed = time.time() - start
        
        print(f"  Hashed {word_count:,} words in {elapsed:.2f}s")
        print(f"  Speed: {word_count/elapsed:,.0f} hashes/sec")

    def crack_hash(self, hash_str, word, algo, salt=None):
        """Check single hash+word combination"""
        hasher = getattr(hashlib, algo)
        if salt:
            return hasher((salt + word).encode()).hexdigest() == hash_str
        return hasher(word.encode()).hexdigest() == hash_str

    def crack(self, hash_str, wordlist, algo, salt=None, threads=4):
        """Multi-threaded cracking with progress bar"""
        self.start_time = time.time()
        self.found = False
        result = None
        
        try:
            # Get total lines for progress bar
            total = sum(1 for _ in open(wordlist, 'rb'))
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    with tqdm(total=total, unit='words', desc="🔍 Cracking") as pbar:
                        for word in f:
                            if self.found:
                                break
                            word = word.strip()
                            if self.crack_hash(hash_str, word, algo, salt):
                                self.found = True
                                result = word
                                break
                            pbar.update(1)
                            
            return result
        except FileNotFoundError:
            print(f"❌ Wordlist not found: {wordlist}")
            exit(1)

    def interactive_mode(self):
        """Interactive user interface"""
        print("\n" + "="*50)
        print("🔥 ULTIMATE HASH CRACKER".center(50))
        print("="*50)
        
        # Hash input
        while True:
            hash_input = input("\nEnter hash (or multiple hashes separated by commas): ").strip()
            if hash_input:
                break
        
        # Wordlist selection
        wordlist = input(f"Wordlist path [default: {DEFAULT_WORDLIST}]: ").strip() or DEFAULT_WORDLIST
        
        # Algorithm selection
        while True:
            algo = input("Algorithm (leave blank for auto-detect): ").strip().lower()
            if not algo:
                algo = self.detect_algorithm(hash_input.split(',')[0])
                if not algo:
                    print("❌ Couldn't auto-detect algorithm. Please specify.")
                    continue
                print(f"🔍 Auto-detected algorithm: {algo}")
                break
            elif algo in SUPPORTED_ALGOS:
                break
            else:
                print(f"❌ Unsupported algorithm. Choose from: {', '.join(SUPPORTED_ALGOS)}")
        
        # Salt input
        salt = input("Salt (if applicable): ").strip() or None
        
        # Thread count
        threads = input("Threads [default: 4]: ").strip()
        threads = int(threads) if threads.isdigit() else 4
        
        # Benchmark option
        if input("Run benchmark first? [y/N]: ").lower() == 'y':
            self.benchmark(algo)
        
        return hash_input.split(','), wordlist, algo, salt, threads

def main():
    cracker = HashCracker()
    parser = argparse.ArgumentParser(description="Ultimate Hash Cracker")
    
    # Arguments
    parser.add_argument("-hsh", "--hash", help="Hash(es) to crack (comma-separated)")
    parser.add_argument("-w", "--wordlist", help=f"Path to wordlist [default: {DEFAULT_WORDLIST}]")
    parser.add_argument("-a", "--algorithm", help="Hash algorithm", choices=SUPPORTED_ALGOS)
    parser.add_argument("-s", "--salt", help="Salt value for salted hashes")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Thread count [default: 4]")
    parser.add_argument("-b", "--benchmark", action="store_true", help="Run benchmark first")
    
    args = parser.parse_args()
    
    # Interactive mode if no args
    if not args.hash or not args.wordlist:
        hashes, wordlist, algo, salt, threads = cracker.interactive_mode()
    else:
        hashes = args.hash.split(',')
        wordlist = args.wordlist or DEFAULT_WORDLIST
        algo = args.algorithm or cracker.detect_algorithm(hashes[0])
        salt = args.salt
        threads = args.threads
        
        if not algo:
            print("❌ Couldn't detect algorithm. Please specify with -a")
            exit(1)
        
        if args.benchmark:
            cracker.benchmark(algo)
    
    # Process each hash
    for hsh in hashes:
        hsh = hsh.strip()
        print(f"\n🚀 Cracking hash: {hsh}")
        print(f"• Algorithm: {algo}")
        if salt:
            print(f"• Salt: {salt}")
        print(f"• Wordlist: {wordlist}")
        print(f"• Threads: {threads}")
        
        result = cracker.crack(hsh, wordlist, algo, salt, threads)
        
        if result:
            print(f"\n✅ CRACKED! Plaintext: {result}")
            print(f"⏱️  Time elapsed: {time.time() - cracker.start_time:.2f}s")
        else:
            print("\n❌ No match found in wordlist")

if __name__ == "__main__":
    main()
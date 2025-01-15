use std::fs::File;
use std::io::{self, BufRead, Write};
use std::path::Path;

fn supasecurefibberdachicheckerthing(n: usize) -> Vec<u64> {
    let mut fib: Vec<u64> = vec![0, 1];
    for i in 2..n {
        let next = fib[i - 1].checked_add(fib[i - 2]).unwrap_or(0);
        fib.push(next);
    }
    fib
}

fn validate_license_key(key: &str) -> bool {
    if !key.starts_with("XMAS") {
        return false;
    }

    if key.len() != 12 {
        return false;
    }

    let ascii_sum: u32 = key.chars().skip(4).take(5).map(|c| c as u32).sum();
    if ascii_sum != 610 {
        return false;
    }

    let fib_482 = supasecurefibberdachicheckerthing(483)[482];
    let fib_last_3 = fib_482 % 1000;

    let key_last_3: u16 = match key[9..12].parse() {
        Ok(num) => num,
        Err(_) => return false,
    };

    if key_last_3 != fib_last_3 as u16 {
        return false;
    }

    true
}

fn win() {
    let flag_path = Path::new("flag.txt");

    if let Ok(file) = File::open(flag_path) {
        let mut buf_reader = io::BufReader::new(file);
        let mut flag = String::new();
        if buf_reader.read_line(&mut flag).is_ok() {
            println!("🎄 Ho Ho Ho!, go watch some ELFTV!: {}", flag.trim());
        } else {
            println!("smth went wrong contact vip3r with error (flag-file-1)");
        }
    } else {
        println!("smth went wrong contact vip3r with error (flag-file-2)");
    }
}


fn main() {
    println!("🎄 Welcome to the ElfTV XMAS-license key checker!");
    println!("Please enter your license key:");

    let stdin = io::stdin();
    let mut input = String::new();
    let mut stdout = io::stdout();

    if stdin.read_line(&mut input).is_ok() {
        let key = input.trim();
        if validate_license_key(key) {
            win();
        } else {
            writeln!(stdout, "Ho ho ho! Try again.").unwrap();
        }
    } else {
        writeln!(stdout, "Failed to read the input!").unwrap();
    }
}
; baby-emulator crate README — countdown loop (modern notation)
; https://docs.rs/baby-emulator/0.2.1/baby_emulator/
; Catalog: programs/baby_rust_countdown.store

ldn $start_value

:loop_start_value
sub $subtract_val
cmp
jmp $loop_start
stp

:loop_start
abs $loop_start_value

:subtract_val
abs 0d1

:start_value
abs 0d-10

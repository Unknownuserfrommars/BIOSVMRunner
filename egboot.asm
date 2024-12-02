jmp $              ; Infinite loop
times 510-($-$$) db 0x00 ; Fill the rest of the sector with zeros
db 0x55, 0xAA      ; Boot sector signature
; 这是我们第二个视频中向大家展示的一个简单的引导扇区。我们当时使用了NASM来编译它。我已经将它提前编译好了，我会考虑将源代码上传到GitHub上。
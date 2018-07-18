`timescale 1ns / 1ps

// CD4013B: dual D-type flip-flops
module cd4013b(
  input clk,
  input data,
  input set,
  input reset,
  output reg q,
  output nq
  );
    
    assign nq = ~q;

    initial begin
        q = 0;
    end
    
    always @(posedge clk or posedge set or posedge reset) begin
        if(set) q <= 1;
        else if(reset) q <= 0;
        else q <= data;
    end
    
endmodule // cd4013b

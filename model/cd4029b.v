`timescale 1ns / 1ps

// CD4029B: presettable up/down counter
module cd4029b(
  input clk,
  input [3:0] preset,
  input cin_n,
  input preset_en,
  input bin_dec,
  input up_down,
  output reg [3:0] count,
  output cout_n
  );

    wire bin_cout = (count == (up_down ? 4'b1111 : 4'b0000)) ? 1'b1 : 1'b0;
    wire dec_cout = (count == (up_down ? 4'd9 : 4'd0)) ? 1'b1 : 1'b0;
    assign cout_n = ~(~cin_n & bin_dec ? bin_cout : dec_cout);

    initial begin
        count = 4'b0000;
    end
    
    always @(posedge clk or posedge preset_en) begin
        if(preset_en) begin
            count <= preset;
        end else if(~cin_n) begin
            if(up_down) begin
                if(~cout_n) count <= 4'b0;
                else count <= count + 4'b1;
            end else begin
                if(~cout_n & ~bin_dec) count <= 4'd9;
                else count <= count - 4'b1;
            end
        end
    end
    
endmodule // cd4029b

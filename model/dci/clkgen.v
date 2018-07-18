`include "cd4013b.v"
`include "cd4029b.v"

`timescale 1ns / 1ps

module clkgen(
  input clk_in,
  input en_300_n,
  input en_600_n,
  input en_1200_n,
  output clk_out
  );

    wire preset;
    wire cnt0_cout_n, cnt1_cout_n;
    wire ff0_q, ff0_nq, ff1_nq;
    
    cd4029b cnt0(
      .clk(clk_in),
      .preset({~en_300_n,en_1200_n,en_300_n,en_600_n}),
      .cin_n(1'b0),
      .preset_en(preset),
      .bin_dec(1'b1),
      .up_down(1'b1),
      .count(),
      .cout_n(cnt0_cout_n)
      );
    cd4029b cnt1(
      .clk(clk_in),
      .preset({1'b1,1'b1,en_300_n,~en_1200_n}),
      .cin_n(cnt0_cout_n),
      .preset_en(preset),
      .bin_dec(1'b1),
      .up_down(1'b1),
      .count(),
      .cout_n(cnt1_cout_n)
      );
    cd4013b ff0(
      .clk(~clk_in),
      .data(cnt1_cout_n),
      .set(1'b0),
      .reset(1'b0),
      .q(ff0_q),
      .nq(ff0_nq)
      );
    cd4013b ff1(
      .clk(ff0_q),
      .data(ff1_nq),
      .set(1'b0),
      .reset(1'b0),
      .q(clk_out),
      .nq(ff1_nq)
      );
    and and0(preset, ff0_nq, clk_in);
    
endmodule // clkgen

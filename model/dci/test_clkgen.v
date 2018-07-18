`include "dci/clkgen.v"

`timescale 1ps / 1ps

module test_clkgen();
    
    reg clk_in, en_300_n, en_600_n, en_1200_n;
    wire clk_out;
    clkgen uut(.*);
    
    initial begin
        $dumpvars;
        
        clk_in = 0;
        en_300_n = 1;  // actual:  301.2Hz (0.4% error)
        en_600_n = 1;  // actual:  590.8Hz (1.5% error)
        en_1200_n = 0; // actual: 1181.5Hz (1.5% error)
        
        // Input clock is 11.7965MHz divided by 2, then 12
        // (2*12)/11796500 = ~0.000002034502s = 2034502ps
        // 2034502ps / 2 = 1017251ps
        forever begin
            #1017251;
            clk_in = 1;
            #1017251;
            clk_in = 0;
        end
    end
    
endmodule // top

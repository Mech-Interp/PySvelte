import { setBackend, ones } from "@tensorflow/tfjs";
import { render, screen } from "@testing-library/react";
import React from "react";
import { AttentionPatterns, colorAttentionTensors } from "../AttentionPatterns";

beforeAll(() => {
  // Use the node backend whilst testing
  setBackend("cpu");
});

describe("colorAttentionTensors", () => {
  it("creates a tensor of the correct shape", () => {
    // Input with 2 tokens, 2 heads
    const input = [
      [
        [1, 0],
        [0.5, 0.5]
      ],
      [
        [1, 0],
        [0.5, 0.5]
      ]
    ];

    const res = colorAttentionTensors(input);
    expect(res.shape).toEqual([2, 2, 2, 3]);
  });
});

describe("AttentionPatterns", () => {
  it("renders", () => {
    const tokens = ["A", "B", "C", "D"];
    const attention = ones([4, 4, 16]);

    render(
      <AttentionPatterns
        tokens={JSON.stringify(tokens)}
        attention={JSON.stringify(attention.arraySync())}
      />
    );

    // Check the header text loads
    screen.getByText("Attention Patterns");
  });
});

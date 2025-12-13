import { describe, it, expect } from 'vitest';
import { INITIAL_SCORE, increaseScore, decreaseScore, resetScore } from './score';

describe('score utilities', () => {
  it('INITIAL_SCORE should be 0', () => {
    expect(INITIAL_SCORE).toBe(0);
  });

  it('increaseScore should increment the score by 10', () => {
    expect(increaseScore(0)).toBe(10);
    expect(increaseScore(50)).toBe(60);
  });

  it('decreaseScore should decrement the score by 5', () => {
    expect(decreaseScore(10)).toBe(5);
    expect(decreaseScore(50)).toBe(45);
  });

  it('decreaseScore should not go below 0', () => {
    expect(decreaseScore(3)).toBe(0);
    expect(decreaseScore(0)).toBe(0);
  });

  it('resetScore should return the initial score', () => {
    expect(resetScore()).toBe(INITIAL_SCORE);
    expect(resetScore()).toBe(0);
  });
});
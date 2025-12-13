/**
 * The initial score for the game.
 */
export const INITIAL_SCORE = 0;

/**
 * Increases the current score by a default amount.
 * @param currentScore The player's current score.
 * @returns The new score after incrementing.
 */
export function increaseScore(currentScore: number): number {
  // You can customize the score increment amount here
  const scoreIncrement = 10;
  return currentScore + scoreIncrement;
}

/**
 * Resets the score to its initial value.
 * @returns The initial score.
 */
export function resetScore(): number {
  return INITIAL_SCORE;
}

/**
 * Decreases the current score by a default amount.
 * This can be used for penalties, e.g., hitting a branch.
 * @param currentScore The player's current score.
 * @returns The new score after decrementing. Will not go below 0.
 */
export function decreaseScore(currentScore: number): number {
  // You can customize the score decrement amount here
  const scoreDecrement = 5;
  return Math.max(0, currentScore - scoreDecrement);
}
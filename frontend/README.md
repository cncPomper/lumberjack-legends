# Lumberjack Legends Frontend

Welcome to the frontend application for Lumberjack Legends! This project is built with Vite, TypeScript, React, shadcn-ui, and Tailwind CSS.

## Project Setup

### Prerequisites

*   Node.js (LTS version recommended)
*   npm (comes with Node.js) or Bun

### Installation

Navigate to the `frontend` directory and install dependencies:

```bash
cd /workspaces/lumberjack-legends/frontend
npm install
# or if you use Bun
# bun install
```

## Running the Application

To start the development server:

```bash
cd /workspaces/lumberjack-legends/frontend
npm run dev
# or if you use Bun
# bun dev
```

This will usually open the application in your browser at `http://localhost:8080`.

## Running Tests

This project uses [Vitest](https://vitest.dev/) for testing.

### Test Scripts

The `package.json` includes the following test scripts for convenience:

*   `npm run test`: Runs tests in watch mode (interactive).
*   `npm run test:run`: Runs all tests once and exits.

### How to Run Tests

1.  **Ensure Dependencies are Installed**:
    ```bash
    cd /workspaces/lumberjack-legends/frontend
    npm install # or bun install
    ```

2.  **Run All Tests (once)**:
    ```bash
    cd /workspaces/lumberjack-legends/frontend
    npm run test:run
    # or using npx/bun directly if script not added:
    # npx vitest --run
    # bun vitest --run
    ```

3.  **Run Tests in Watch Mode (interactive)**:
    ```bash
    cd /workspaces/lumberjack-legends/frontend
    npm run test
    # or using npx/bun directly if script not added:
    # npx vitest
    # bun vitest
    ```

4.  **Run a Specific Test File**:
    Replace `<path/to/your/test.ts>` with the actual path to the test file.
    ```bash
    cd /workspaces/lumberjack-legends/frontend
    npm exec vitest -- src/services/mockApi.integration.test.ts --run
    # Example for a specific component test:
    # npm exec vitest -- src/components/game/GameHUD.test.tsx --run
    ```

### Test Environment

Tests are configured to run in a `jsdom` environment, which simulates a browser DOM for React component testing.
The `setupTests.ts` file is used for global test setup, e.g., extending `expect` with `@testing-library/jest-dom` matchers.

---

## What technologies are used for this project?

-   **Vite**: Fast frontend tooling, development server, and build tool.
-   **TypeScript**: Statically typed superset of JavaScript.
-   **React**: A JavaScript library for building user interfaces.
-   **shadcn-ui**: A collection of re-usable components for React.
-   **Tailwind CSS**: A utility-first CSS framework for rapidly building custom designs.

## Additional Information

For more details on deploying this project or connecting a custom domain, refer to the original project documentation if available.
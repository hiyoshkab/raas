import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import App from "./App";

describe("App", () => {
  it("shows the selected filename", async () => {
    const user = userEvent.setup();
    render(<App />);

    const file = new File(["Hello"], "notes.txt", { type: "text/plain" });
    await user.upload(
      screen.getByLabelText("Choose a .txt or .md file"),
      file,
    );

    expect(screen.getByText("notes.txt")).toBeTruthy();
  });
});
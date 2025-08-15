import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Progress } from '../Progress';

describe('Progress', () => {
  it('renders the progress bar', () => {
    render(<Progress value={50} />);
    const progressBar = screen.getByRole('progressbar');
    expect(progressBar).toBeInTheDocument();
  });

  it('updates the indicator style based on the value', () => {
    const { container } = render(<Progress value={30} />);
    const indicator = container.querySelector('[role="progressbar"] > div');
    expect(indicator).toHaveStyle('transform: translateX(-70%)');
  });

  it('handles a value of 0', () => {
    const { container } = render(<Progress value={0} />);
    const indicator = container.querySelector('[role="progressbar"] > div');
    expect(indicator).toHaveStyle('transform: translateX(-100%)');
  });

  it('handles a value of 100', () => {
    const { container } = render(<Progress value={100} />);
    const indicator = container.querySelector('[role="progressbar"] > div');
    // Handle -0% case for floating point precision
    expect(indicator).toHaveStyle('transform: translateX(-0%)');
  });
});

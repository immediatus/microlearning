import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Button } from '../Button';

describe('Button', () => {
  it('renders the button with the correct text', () => {
    render(<Button>Click me</Button>);
    const buttonElement = screen.getByRole('button', { name: /Click me/i });
    expect(buttonElement).toBeInTheDocument();
  });

  it('applies the primary variant class by default', () => {
    render(<Button>Click me</Button>);
    const buttonElement = screen.getByRole('button', { name: /Click me/i });
    expect(buttonElement).toHaveClass('bg-blue-600');
  });

  it('applies the destructive variant class when specified', () => {
    render(<Button variant="destructive">Delete</Button>);
    const buttonElement = screen.getByRole('button', { name: /Delete/i });
    expect(buttonElement).toHaveClass('bg-red-600');
  });

  it('is disabled when the disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>);
    const buttonElement = screen.getByRole('button', { name: /Disabled/i });
    expect(buttonElement).toBeDisabled();
  });

  it('renders with the correct age-adaptive class', () => {
    render(<Button ageGroup="5-8">For Kids</Button>);
    const buttonElement = screen.getByRole('button', { name: /For Kids/i });
    expect(buttonElement).toHaveClass('text-lg py-3 px-6');
  });
});

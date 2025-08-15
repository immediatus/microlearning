import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Input } from '../Input';

describe('Input', () => {
  it('renders the input element', () => {
    render(<Input />);
    const inputElement = screen.getByRole('textbox');
    expect(inputElement).toBeInTheDocument();
  });

  it('displays the correct placeholder text', () => {
    render(<Input placeholder="Enter text here" />);
    const inputElement = screen.getByPlaceholderText('Enter text here');
    expect(inputElement).toBeInTheDocument();
  });

  it('is disabled when the disabled prop is true', () => {
    render(<Input disabled />);
    const inputElement = screen.getByRole('textbox');
    expect(inputElement).toBeDisabled();
  });

  it('renders with the correct age-adaptive class', () => {
    render(<Input ageGroup="5-8" />);
    const inputElement = screen.getByRole('textbox');
    expect(inputElement).toHaveClass('text-lg py-3 px-4');
  });

  it('renders with the default age-adaptive class', () => {
    render(<Input />);
    const inputElement = screen.getByRole('textbox');
    expect(inputElement).toHaveClass('text-base py-2 px-3');
  });
});

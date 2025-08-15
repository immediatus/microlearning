import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Spinner } from '../Spinner';

describe('Spinner', () => {
  it('renders the spinner', () => {
    const { container } = render(<Spinner data-testid="spinner" />);
    const spinner = container.querySelector('svg');
    expect(spinner).toBeInTheDocument();
  });

  it('applies size classes correctly', () => {
    const { container } = render(<Spinner size="lg" />);
    const spinner = container.querySelector('svg');
    expect(spinner).toHaveClass('h-12 w-12');
  });

  it('applies default size classes correctly', () => {
    const { container } = render(<Spinner />);
    const spinner = container.querySelector('svg');
    expect(spinner).toHaveClass('h-8 w-8');
  });
});

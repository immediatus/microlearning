import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Badge } from '../Badge';

describe('Badge', () => {
  it('renders the badge with the correct text', () => {
    render(<Badge>Active</Badge>);
    const badgeElement = screen.getByText('Active');
    expect(badgeElement).toBeInTheDocument();
  });

  it('applies the default variant class by default', () => {
    render(<Badge>Default Badge</Badge>);
    const badgeElement = screen.getByText('Default Badge');
    expect(badgeElement).toHaveClass('bg-blue-600');
  });

  it('applies the destructive variant class when specified', () => {
    render(<Badge variant="destructive">Destructive Badge</Badge>);
    const badgeElement = screen.getByText('Destructive Badge');
    expect(badgeElement).toHaveClass('bg-red-600');
  });

  it('applies the success variant class when specified', () => {
    render(<Badge variant="success">Success Badge</Badge>);
    const badgeElement = screen.getByText('Success Badge');
    expect(badgeElement).toHaveClass('bg-green-600');
  });
});

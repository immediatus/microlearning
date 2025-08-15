import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Avatar, AvatarImage, AvatarFallback } from '../Avatar';

describe('Avatar', () => {
  // JSDOM doesn't load images, so Radix's Avatar will always show the fallback.
  // We test that the fallback is correctly rendered.
  it('renders the fallback text', () => {
    render(
      <Avatar>
        <AvatarImage src="test-image.jpg" alt="Test Avatar" />
        <AvatarFallback>JD</AvatarFallback>
      </Avatar>
    );
    const fallbackElement = screen.getByText('JD');
    expect(fallbackElement).toBeInTheDocument();
  });

  it('renders only the fallback when no image is provided', () => {
    render(
      <Avatar>
        <AvatarFallback>JD</AvatarFallback>
      </Avatar>
    );
    const fallbackElement = screen.getByText('JD');
    expect(fallbackElement).toBeInTheDocument();
  });
});

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
} from '../Card';

describe('Card', () => {
  it('renders all sub-components with correct content', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Test Title</CardTitle>
          <CardDescription>Test Description</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Main content goes here.</p>
        </CardContent>
        <CardFooter>
          <p>Footer content</p>
        </CardFooter>
      </Card>
    );

    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('Main content goes here.')).toBeInTheDocument();
    expect(screen.getByText('Footer content')).toBeInTheDocument();
  });

  it('applies the correct base classes to the components', () => {
    const { container } = render(
      <Card>
        <CardHeader>
          <CardTitle>Title</CardTitle>
        </CardHeader>
      </Card>
    );

    // The first child of the container should be the Card component
    const cardElement = container.firstChild;
    expect(cardElement).toHaveClass('rounded-lg border bg-white');

    // Find the header and title to check their classes
    const headerElement = screen.getByText('Title').parentElement;
    expect(headerElement).toHaveClass('flex flex-col');
    const titleElement = screen.getByText('Title');
    expect(titleElement).toHaveClass('text-2xl font-semibold');
  });
});

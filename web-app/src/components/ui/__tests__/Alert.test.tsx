import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Alert, AlertTitle, AlertDescription } from '../Alert';

describe('Alert', () => {
  it('renders the alert with title and description', () => {
    render(
      <Alert>
        <AlertTitle>Heads up!</AlertTitle>
        <AlertDescription>
          You can add components to your app using the cli.
        </AlertDescription>
      </Alert>
    );

    expect(screen.getByText('Heads up!')).toBeInTheDocument();
    expect(
      screen.getByText('You can add components to your app using the cli.')
    ).toBeInTheDocument();
  });

  it('has the role of "alert"', () => {
    render(<Alert />);
    const alertElement = screen.getByRole('alert');
    expect(alertElement).toBeInTheDocument();
  });

  it('applies the destructive variant class when specified', () => {
    render(
      <Alert variant="destructive">
        <AlertTitle>Error</AlertTitle>
      </Alert>
    );
    const alertElement = screen.getByRole('alert');
    expect(alertElement).toHaveClass('border-red-500/50');
  });
});

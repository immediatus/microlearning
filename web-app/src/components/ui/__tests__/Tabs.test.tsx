import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../Tabs';

describe('Tabs', () => {
  it('switches tabs on click', async () => {
    const user = userEvent.setup();
    render(
      <Tabs defaultValue="account">
        <TabsList>
          <TabsTrigger value="account">Account</TabsTrigger>
          <TabsTrigger value="password">Password</TabsTrigger>
        </TabsList>
        <TabsContent value="account">
          Account content
        </TabsContent>
        <TabsContent value="password">
          Password content
        </TabsContent>
      </Tabs>
    );

    // Initially, account tab is active
    expect(screen.getByText('Account content')).toBeInTheDocument();
    expect(screen.queryByText('Password content')).not.toBeInTheDocument();

    // Click on the password tab using userEvent
    await user.click(screen.getByText('Password'));

    // Now, password tab should be active and account tab should be gone
    expect(await screen.findByText('Password content')).toBeInTheDocument();
    expect(screen.queryByText('Account content')).not.toBeInTheDocument();
  });
});

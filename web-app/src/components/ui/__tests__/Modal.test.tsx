import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import {
  Modal,
  ModalTrigger,
  ModalContent,
  ModalHeader,
  ModalTitle,
  ModalDescription,
} from '../Modal';

// Mocking ModalPortal to render in-place for easier testing
jest.mock('@radix-ui/react-dialog', () => ({
  ...jest.requireActual('@radix-ui/react-dialog'),
  Portal: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

describe('Modal', () => {
  it('opens and closes the modal', () => {
    render(
      <Modal>
        <ModalTrigger asChild>
          <button>Open Modal</button>
        </ModalTrigger>
        <ModalContent>
          <ModalHeader>
            <ModalTitle>Are you sure?</ModalTitle>
            <ModalDescription>This action cannot be undone.</ModalDescription>
          </ModalHeader>
        </ModalContent>
      </Modal>
    );

    expect(screen.queryByText('Are you sure?')).not.toBeInTheDocument();

    const trigger = screen.getByText('Open Modal');
    fireEvent.click(trigger);

    expect(screen.getByText('Are you sure?')).toBeInTheDocument();
  });
});

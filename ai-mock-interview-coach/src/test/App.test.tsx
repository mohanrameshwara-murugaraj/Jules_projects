import { test, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AppShell } from '../components/layout/AppShell';

// Mock Auth context so we don't need Supabase setup
vi.mock('@/features/auth/AuthProvider', () => ({
  useAuth: () => ({
    user: { email: 'test@example.com' },
    signOut: vi.fn(),
  }),
}));

test('renders AppShell component', () => {
  render(
    <BrowserRouter>
      <AppShell>
        <div>Test Content</div>
      </AppShell>
    </BrowserRouter>
  );

  expect(screen.getByText('Test Content')).toBeInTheDocument();
  expect(screen.getAllByText('AI Coach')[0]).toBeInTheDocument(); // Sidebar/Mobile text
});
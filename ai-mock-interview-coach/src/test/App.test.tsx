import { test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { AppShell } from '../components/layout/AppShell';

test('renders AppShell component', () => {
  render(
    <AppShell>
      <div>Test Content</div>
    </AppShell>
  );

  expect(screen.getByText('Test Content')).toBeInTheDocument();
  expect(screen.getByText('AI Coach')).toBeInTheDocument(); // Sidebar text
});
import { NextPage } from 'next'
import styled from 'styled-components'
import UiContainer from '@/components/Ui/Container/UiContainer'
import React from 'react'
import UiButton from '@/components/Ui/Button/UiButton'
import UiDrawer from '@/components/Ui/Drawer/UiDrawer'
import UiLink from '@/components/Ui/Link/UiLink'
/**
 * `UiDrawerExample` is an example page for the {@link UiDrawer} component.
 */
const UiDrawerExample: NextPage = () => {
  return (
    <UiContainer>
      <Heading>
        <Code>UiDrawer</Code> Examples
      </Heading>

      <SpacedSection>
        <div>
          <UiDrawer>
            <UiDrawer.Trigger>{({ open }) => (
              <UiButton onClick={open}>
                Simple Drawer
              </UiButton>
            )}</UiDrawer.Trigger>
            <UiDrawer.Body>
              I am a drawer!
            </UiDrawer.Body>
          </UiDrawer>
          <p>
            A drawer is a variation of a <UiLink href="./ui-modal">modal</UiLink>.
            Instead of showing a centered window, the drawer creates a full-height element that slides in from the side.
          </p>
          <p>
            This page does not contain all possible options of the drawer components, as its basically the same API
            as for modals - you just need to replace <Code>UiModal</Code> with <Code>UiDrawer</Code>.
          </p>
          <p>
            Features unique to drawers will be explained on this page.
            <br />
            Features unique to modals are listed here:
          </p>
          <ul>
            <li>Built-in title</li>
          </ul>
        </div>
        <div>
          <p>
            Some Examples for drawers:
          </p>
          <UiDrawer size="full">
            <UiDrawer.Trigger>{({ open }) => (
              <UiButton onClick={open}>
                Full-Size Drawer
              </UiButton>
            )}</UiDrawer.Trigger>
            <UiDrawer.Body>
              I am a full-size drawer!
            </UiDrawer.Body>
          </UiDrawer>

          <UiDrawer>
            <UiDrawer.Trigger>{({ open }) => (
              <UiButton onClick={open}>
                Nested Drawers
              </UiButton>
            )}</UiDrawer.Trigger>
            <UiDrawer.Body>
              <UiDrawer>
                <UiDrawer.Trigger>{({ open }) => (
                  <UiButton onClick={open}>
                    Open me!
                  </UiButton>
                )}</UiDrawer.Trigger>
                <UiDrawer.Body>
                  I am a nested drawer!
                </UiDrawer.Body>
              </UiDrawer>
            </UiDrawer.Body>
          </UiDrawer>

          <UiDrawer isPersistent>
            <UiDrawer.Trigger>{({ open }) => (
              <UiButton onClick={open}>
                Persistent Drawer
              </UiButton>
            )}</UiDrawer.Trigger>
            <UiDrawer.Body>
              I am persistent!
            </UiDrawer.Body>
          </UiDrawer>
        </div>

        <div>
          <UiDrawer position="right">
            <UiDrawer.Trigger>{({ open }) => (
              <UiButton onClick={open}>
                Right-aligned Drawer
              </UiButton>
            )}</UiDrawer.Trigger>
            <UiDrawer.Body>
              I appear from the right!
            </UiDrawer.Body>
          </UiDrawer>
          <p>
            The position of a drawer can be set with the <Code>position</Code> property.
            By default, drawers will use <Code>position=&quot;left&quot;</Code>.
          </p>
        </div>
      </SpacedSection>
    </UiContainer>
  )
}
export default UiDrawerExample


const Heading = styled.h1`
  font-size: 2rem;
  margin-top: 3rem;
`

const SpacedSection = styled.section`
  margin-top: 1rem;
  display: inline-flex;
  flex-direction: column;
  gap: 2rem;
  max-width: 60rem;
  
  & > div {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    
    em {
      font-style: italic;
    }
    
    ul {
      list-style: disc;
      margin-left: 1rem;
      margin-top: 0.5rem;
    }
  }
`

const Code = styled.code`
  font-family: Consolas, monospace;
`

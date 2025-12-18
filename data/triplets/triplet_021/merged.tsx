import React from 'react'
import styled from 'styled-components'
import UiLink from '@/components/Ui/Link/UiLink'
import Image from 'next/image'

/**
 * `PageFooter` represents the footer on the bottom of each page.
 */
const PageFooter: React.VFC = () => {
  return (
    <FooterContainer>
      <UiLink href="https://rfobaden.ch/" target="_blank" isText>
        RFO Baden
      </UiLink>

      &copy; {new Date().getFullYear()} RFO Baden

      <UiLink href="https://www.fhnw.ch/de/" target="_blank">
        <Image src="/fhnw-logo.svg" alt="FHNW Logo" width="108" height="25" />
      </UiLink>
    </FooterContainer>
  )
}
export default PageFooter

const FooterContainer = styled.footer`
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 4rem;
  padding: 10px 50px;
  margin-top: 2rem;
  background: ${({ theme }) => theme.colors.tertiary.value};
  font-size: 0.8em;
`

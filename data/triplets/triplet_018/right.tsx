import React, { ReactNode, useMemo } from 'react'
import UiContainer from '@/components/Ui/Container/UiContainer'
import UiTitle from '@/components/Ui/Title/UiTitle'
import UiGrid, { ColSizeProp } from '@/components/Ui/Grid/UiGrid'
import styled from 'styled-components'
import UiIcon from '@/components/Ui/Icon/UiIcon'
import UiLink from '@/components/Ui/Link/UiLink'
import { GetServerSideProps } from 'next'
import { BackendResponse, getSessionFromRequest } from '@/services/BackendService'
import Incident, { isClosedIncident, parseIncident } from '@/models/Incident'
import { useEffectOnce } from 'react-use'
import IncidentStore, { useIncidents } from '@/stores/IncidentStore'
import { Themed } from '@/theme'
import Page from '@/components/Page/Page'

interface Props {
  data: {
    /**
     * List of {@link Incident incidents}.
     */
    incidents: Incident[]
  }
}

/**
 * `HomePage` is the landing page.
 */
const HomePage: React.VFC<Props> = ({ data }) => {
  useEffectOnce(() => {
    IncidentStore.saveAll(data.incidents.map(parseIncident))
  })

  const firstIncident = useIncidents().find((it) => !isClosedIncident(it)) ?? null

  const dashboardPanels = useMemo(() => {
    const panels = [
      { icon: UiIcon.IncidentManagement, label: 'Ereignisse', link: '/ereignisse' },
      { icon: UiIcon.UserManagement, label: 'Benutzer', link: '/benutzer' },
      { icon: UiIcon.Organization, label: 'Organisationen', link: '/organisationen' },
      { icon: UiIcon.Archive, label: 'Archiv', link: '/ereignisse/archiv' },
    ]
    if (firstIncident !== null) {
      // Only show transport panel if there is at least one open incident.
      panels.splice(1, 0, {
        icon: UiIcon.Transport,
        label: 'Transporte',
        link: `/ereignisse/${firstIncident.id}/transporte`,
      })
    }
    return panels
  }, [firstIncident])

  return (
    <Page>
      <UiContainer>
        <UiTitle level={1} isCentered>
          {/*//TODO make responsive - title does not break yet*/}
          <Bold>INCIDENT</Bold><Light>MANAGER</Light>
        </UiTitle>
        <Subtitle>
          Regionales Führungsorgan Baden
        </Subtitle>
        <Panels>
          <UiGrid gap={1.5} justify="center">
            {dashboardPanels.map((card, i) => (
              <CardColumn
                key={i}
                size={{ xs: 12, sm: (i < 2 || dashboardPanels.length % 2 === 0) ? 6 : 4 }}
                card={card}
                icon={<card.icon size={5} />}
              />
            ))}
          </UiGrid>
        </Panels>
      </UiContainer>
    </Page>
  )
}
export default HomePage

interface CardProps {
  size: ColSizeProp
  card: {
    label: string
    link: string
  }
  icon: ReactNode
}

const CardColumn: React.VFC<CardProps> = ({
  size,
  card,
  icon,
}) => {
  return (
    <UiGrid.Col key={card.label} size={size}>
      <UiLink href={card.link}>
        <Card>
          {icon}
          <CardTitle level={4}>{card.label}</CardTitle>
        </Card>
      </UiLink>
    </UiGrid.Col>
  )
}

const Subtitle = styled.div`
  width: 100%;
  text-align: center;
  //margin-top: 0.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
`

const Bold = styled.span`
 font-weight: bolder; 
 `
const Light = styled.span`
 font-weight: lighter; 
 `

const Card = styled.div`
  height: 15rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: ${({ theme }) => theme.colors.secondary.contrast};
  background-color: ${({ theme }) => theme.colors.secondary.value};

  border-radius: 0.5rem;

  transition: 250ms ease;
  transition-property: background-color;

  :hover:not(&[disabled]), :active:not(&[disabled]) {
    cursor: pointer;
    background-color: ${({ theme }) => theme.colors.secondary.hover};
  }
`

const CardTitle = styled(UiTitle)`
  text-align: center;
`

const Panels = styled.div`
  display: flex;
  justify-content: center;

  & > ${UiGrid} {
    ${Themed.media.lg.min} {
      width: 80%;
    }

    ${Themed.media.xl.min} {
      width: 60%;
    }
  }
`

export const getServerSideProps: GetServerSideProps = async ({ req }) => {
  const { user, backendService } = getSessionFromRequest(req)
  if (user === null) {
    return { redirect: { statusCode: 302, destination: '/anmelden' }}
  }

  const [incidents, incidentsError]: BackendResponse<Incident[]> = await backendService.list('incidents')
  if (incidentsError !== null) {
    throw incidentsError
  }

  return {
    props: {
      data: {
        incidents,
      },
    },
  }
}

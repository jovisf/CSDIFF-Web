import React from 'react'
import { isAdmin } from '@/models/User'
import UiList from '@/components/Ui/List/UiList'
import UiDrawer from '@/components/Ui/Drawer/UiDrawer'
import UiCreatButton from '@/components/Ui/Button/UiCreateButton'
import UiIcon from '@/components/Ui/Icon/UiIcon'
import UiTitle from '@/components/Ui/Title/UiTitle'
import UiGrid from '@/components/Ui/Grid/UiGrid'
import UiSortButton from '@/components/Ui/Button/UiSortButton'
import useSort from '@/utils/hooks/useSort'
import { useCurrentUser } from '@/stores/SessionStore'
import Organization from '@/models/Organization'
import OrganizationForm from '@/components/Organization/Form/OrganizationForm'
import OrganizationListItem from '@/components/Organization/List/Item/OrganizationListItem'
import styled from 'styled-components'
import { Themed } from '@/theme'

interface Props {

  /**
   * The {@link Organization organizations} to be displayed.
   */
  organizations: readonly Organization[]

  /**
   * Displays a Button to create new {@link Organization organizations}.
   */
  hasCreateButton?: boolean
}

/**
 * `OrganizationList` is a component that displays a list of {@link Organization organizations}.
 */
const OrganizationList: React.VFC<Props> = ({ organizations, hasCreateButton = false }) => {
  const currentUser = useCurrentUser()

  const [sortedOrganizations, sort] = useSort(organizations, () => ({
    name: String,
    userCount: ({ userIds: a }, { userIds: b }) => {
      if (a.length === b.length) {
        return 0
      }
      if (a.length < b.length) {
        return -1
      } else {
        return 1
      }
    },
  }))

  return (
    <OuterScroll>
      <InnerScroll>
        {isAdmin(currentUser) && hasCreateButton && (
          <UiDrawer title="Organisation erfassen" size="fixed">
            <UiDrawer.Trigger>{({ open }) => (
              <UiCreatButton onClick={open}>
                <UiIcon.CreateAction size={1.4} />
              </UiCreatButton>
            )}</UiDrawer.Trigger>
            <UiDrawer.Body>{({ close }) => (
              <OrganizationForm onClose={close} />
            )}</UiDrawer.Body>
          </UiDrawer>
        )}
        <UiGrid style={{ padding: '0.5rem 0.5rem 0rem 0.5rem' }} gapH={0.5}>
          <UiGrid.Col size={7}>
            <UiSortButton field={sort.name}>
              <UiTitle level={6}>Organisation</UiTitle>
            </UiSortButton>
          </UiGrid.Col>
          <UiGrid.Col textAlign="right" size={4}>
            <UiSortButton field={sort.userCount}>
              <UiTitle level={6}>Anzahl Benutzer</UiTitle>
            </UiSortButton>
          </UiGrid.Col>
        </UiGrid>

        <UiList>
          {sortedOrganizations.map((organization) => (
            <OrganizationListItem
              key={organization.id}
              organization={organization}
            />
          ))}
        </UiList>
      </InnerScroll>
    </OuterScroll>
  )
}
export default OrganizationList

const InnerScroll = styled.div`
  ${Themed.media.sm.max} {
    width: 155vw;
  }
`

const OuterScroll = styled.div`
  ${Themed.media.sm.max} {
    overflow-x: scroll;
  }
`
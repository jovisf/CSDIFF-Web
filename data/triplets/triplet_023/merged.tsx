import React from 'react'
import User, { isAdmin } from '@/models/User'
import UiList from '@/components/Ui/List/UiList'
import UiDrawer from '@/components/Ui/Drawer/UiDrawer'
import UiCreateButton from '@/components/Ui/Button/UiCreateButton'
import UiIcon from '@/components/Ui/Icon/UiIcon'
import UiTitle from '@/components/Ui/Title/UiTitle'
import UserForm from '@/components/User/Form/UserForm'
import UserListItem from '@/components/User/List/Item/UserListItem'
import UiGrid from '@/components/Ui/Grid/UiGrid'
import UiSortButton from '@/components/Ui/Button/UiSortButton'
import useSort from '@/utils/hooks/useSort'
import OrganizationStore from '@/stores/OrganizationStore'
import { useCurrentUser } from '@/stores/SessionStore'
import styled from 'styled-components'
import { Themed } from '@/theme'

interface Props {

  /**
   * The {@link User users} to be displayed.
   */
  users: readonly User[]

  /**
   * Whether to show a button with which a {@link UserForm} can be opened.
   */
  hasCreateButton?: boolean
}

/**
 * `UserList` is a component that displays a list of {@link User users}.
 */
const UserList: React.VFC<Props> = ({ users, hasCreateButton = false }) => {
  const currentUser = useCurrentUser()

  const [sortedUsers, sort] = useSort(users, () => ({
    firstName: String,
    lastName: String,
    role: String,
    organization: ({ organizationId: a }, { organizationId: b }) => {
      if (a === b) {
        return 0
      }
      if (a === null) {
        return -1
      }
      if (b === null) {
        return 1
      }
      const aOrg = OrganizationStore.find(a)
      const bOrg = OrganizationStore.find(b)
      if (aOrg === null || bOrg === null) {
        throw new Error('organization not found')
      }
      return aOrg.name.localeCompare(bOrg.name)
    },
  }))

  return (
    <React.Fragment>
      {isAdmin(currentUser) && hasCreateButton && (
        <UiDrawer title="Benutzer erfassen" size="fixed">
          <UiDrawer.Trigger>{({ open }) => (
            <UiCreateButton onClick={open}>
              <UiIcon.CreateAction size={1.4} />
            </UiCreateButton>
          )}</UiDrawer.Trigger>
          <UiDrawer.Body>{({ close }) => (
            <UserForm onClose={close} />
          )}</UiDrawer.Body>
        </UiDrawer>
      )}

      <OuterScroll>
        <InnerScroll>
          <UiGrid style={{ padding: '0.5rem 0.5rem 0rem 0.5rem' }} gapH={0.5}>
            <UiGrid.Col size={5}>
              <UiSortButton field={sort.firstName}>
                <UiTitle level={6}>Vorname</UiTitle>
              </UiSortButton>
              <UiSortButton field={sort.lastName}>
                <UiTitle level={6}>Nachname</UiTitle>
              </UiSortButton>
            </UiGrid.Col>
            <UiGrid.Col size={2}>
              <UiSortButton field={sort.role}>
                <UiTitle level={6}>Rolle</UiTitle>
              </UiSortButton>
            </UiGrid.Col>
            <UiGrid.Col size={4}>
              <UiSortButton field={sort.organization}>
                <UiTitle level={6}>Organisation</UiTitle>
              </UiSortButton>
            </UiGrid.Col>
          </UiGrid>

          <UiList>
            {sortedUsers.map((user) => (
              <UserListItem
                key={user.id}
                user={user}
              />
            ))}
          </UiList>
        </InnerScroll>
      </OuterScroll>
    </React.Fragment>
  )
}
export default UserList

const InnerScroll = styled.div`
  ${Themed.media.xs.only} {
    width: 155vw;
  }
`

const OuterScroll = styled.div`
  ${Themed.media.xs.max} {
    overflow-x: scroll;
  }
`
from cielingo_core.noema_surface.command_prompt import NoemaSurface
from cielingo_core.noema_local_sot_agent.access_control import LocalSOTAccessController, build_default_access_standard


def test_access_standard_exists_and_verifies():
    surface = NoemaSurface('.')
    result = surface.verify_local_sot_access_standard()
    assert result.ok, result.issues
    data = result.payload
    assert data['schema'] == 'NOEMA_LOCAL_SOT_AGENT_ACCESS_STANDARD_V0_1'
    assert data['authority']['local_sot_write_permission_granted_by_user'] is True
    assert data['authority']['external_sot_write_permission_claimed'] is False


def test_write_guard_allows_cielingo_but_blocks_non_work_core_without_allow():
    controller = LocalSOTAccessController('.')
    assert controller.can_write('src/cielingo_core/example.py').ok is True
    blocked = controller.can_write('src/ciel_sot_agent/core.py')
    assert blocked.ok is False
    assert blocked.required_grant == 'ADRIAN_CONDITIONAL_ALLOW'


def test_conditional_allow_can_scope_protected_path():
    controller = LocalSOTAccessController('.')
    grant = {
        'grant_type': 'ADRIAN_CONDITIONAL_ALLOW',
        'status': 'ACTIVE_BY_USER_COMMAND',
        'scope_paths': ['src/ciel_sot_agent/**'],
    }
    assert controller.can_write('src/ciel_sot_agent/core.py', allow_grant=grant).ok is True


def test_key_material_and_allow_form_exist():
    surface = NoemaSurface('.')
    for path in [
        'state/noema_local_sot_agent/keys/public/SOT_AGENT_READONLY_PUBLIC_KEY.json',
        'state/noema_local_sot_agent/keys/private/SOT_AGENT_SUDO_PRIVATE_KEY.json',
        'state/noema_local_sot_agent/keys/allow/SOT_AGENT_ALLOW_FORM_TEMPLATE.json',
        'state/noema_local_sot_agent/keys/PUBLIC_ACCESS_MANIFEST.json',
    ]:
        assert surface.read_json(path).ok, path
    pub = surface.read_json('state/noema_local_sot_agent/keys/public/SOT_AGENT_READONLY_PUBLIC_KEY.json').payload['data']
    assert 'write' in pub['forbidden_capabilities']
    allow = surface.read_json('state/noema_local_sot_agent/keys/allow/SOT_AGENT_ALLOW_FORM_TEMPLATE.json').payload['data']
    assert allow['payload']['status'] == 'TEMPLATE_NOT_ACTIVE'

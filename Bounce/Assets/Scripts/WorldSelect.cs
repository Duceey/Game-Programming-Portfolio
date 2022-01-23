using UnityEngine;
using UnityEngine.SceneManagement;


public class WorldSelect : MonoBehaviour
{
    public int WorldIndex;
    public int BufferIndex = 2;

    public void GoToWorld()
    {
        SceneManager.LoadScene(WorldIndex + BufferIndex);
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class WorldControl : MonoBehaviour
{
    public static WorldControl instance = null;
    int worldIndex, worldComplete;

    private void Start()
    {
        if (instance == null) { instance = this; }
        else if (instance != this) { Destroy(gameObject); }

        worldIndex = SceneManager.GetActiveScene().buildIndex;
        worldComplete = PlayerPrefs.GetInt("WorldComplete");
    }

    public void WorldComplete()
    {
        // add end game scene
        if (worldIndex == 3) { Invoke("loadMainMenu", 0f); }
        else
        {
            if (worldComplete < worldIndex) { PlayerPrefs.SetInt("WorldComplete", worldIndex); }

            Invoke("loadNextWorld", 0f);
        }
    }

    void loadNextWorld()
    {
        SceneManager.LoadScene(worldIndex + 1);
    }

    void loadMainMenu()
    {
        SceneManager.LoadScene("Main Menu");
    }
}
